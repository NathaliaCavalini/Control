from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemHeadlineText
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ColorProperty, ListProperty
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.clock import Clock
from plyer import filechooser
import hashlib
import os
import json
from kivy.lang import Builder

# Importações do banco (crie o arquivo banco.py na mesma pasta)
from banco import criar_banco, salvar_nota, listar_notas, deletar_nota, carregar_nota


class TelaPrincipal(MDScreen):
    def on_start(self):
        criar_banco()
        self.atualizar_lista()

    def atualizar_lista(self):
        self.ids.lista_notas.clear_widgets()
        notas = listar_notas()
        for id_nota, titulo in notas:
            item = MDListItem()
            item.add_widget(MDListItemHeadlineText(text=titulo))
            item.bind(on_release=lambda x, id=id_nota: self.abrir_nota(id))
            self.ids.lista_notas.add_widget(item)

    def abrir_nota(self, id_nota):
        nota = carregar_nota(id_nota)
        if nota.get('senha'):
            self.dialog = MDDialog(
                title="Senha",
                type="custom",
                content_cls=MDTextField(hint_text="Digite a senha", password=True),
                buttons=[
                    MDButton(
                        MDButtonText(text="Cancelar"),
                        style="text",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDButton(
                        MDButtonText(text="OK"),
                        style="text",
                        on_release=lambda x: self.verificar_senha(id_nota)
                    )
                ]
            )
            self.dialog.open()
        else:
            self.carregar_editor(id_nota, nota)

    def verificar_senha(self, id_nota):
        senha_digitada = self.dialog.content_cls.text
        self.dialog.dismiss()
        nota = carregar_nota(id_nota)
        if hashlib.sha256(senha_digitada.encode()).hexdigest() == nota['senha']:
            self.carregar_editor(id_nota, nota)
        else:
            erro_dialog = MDDialog(
                title="Erro",
                text="Senha incorreta!",
                buttons=[
                    MDButton(
                        MDButtonText(text="OK"),
                        style="text",
                        on_release=lambda x: erro_dialog.dismiss()
                    )
                ]
            )
            erro_dialog.open()

    def carregar_editor(self, id_nota, nota):
        editor = self.manager.get_screen('editor')
        editor.id_atual = id_nota
        editor.ids.titulo.text = nota['titulo']
        editor.ids.texto.text = nota['conteudo']
        editor.cor_fundo = nota['cor_fundo']
        editor.cor_texto = nota['cor_texto']
        editor.fonte = nota['fonte']
        editor.wallpaper = nota['wallpaper']
        editor.anexos = nota['anexos']
        editor.ids.anexos_lista.text = "\n".join(nota['anexos']) if nota['anexos'] else ""
        editor.atualizar_checklist(nota['checklist'])
        self.manager.current = 'editor'

    def nova_nota(self):
        editor = self.manager.get_screen('editor')
        editor.id_atual = None
        editor.ids.titulo.text = "Nova Nota"
        editor.ids.texto.text = ""
        editor.cor_fundo = [1, 1, 1, 1]
        editor.cor_texto = [0, 0, 0, 1]
        editor.fonte = "Roboto"
        editor.wallpaper = ""
        editor.anexos = []
        editor.ids.anexos_lista.text = ""
        editor.atualizar_checklist([])
        self.manager.current = 'editor'


class TelaEditor(MDScreen):
    id_atual = None
    cor_fundo = ColorProperty([1, 1, 1, 1])
    cor_texto = ColorProperty([0, 0, 0, 1])
    fonte = StringProperty("Roboto")
    wallpaper = StringProperty("")
    anexos = ListProperty([])
    checklist = ListProperty([])

    def voltar(self):
        self.manager.current = 'principal'

    def salvar(self):
        titulo = self.ids.titulo.text
        texto = self.ids.texto.text
        senha = self.ids.senha.text.strip() if self.ids.senha.text and self.ids.senha.text.strip() else None
        anexos = self.anexos[:]

        checklist = []
        children = self.ids.checklist.children
        for i in range(0, len(children), 2):
            cb = children[i + 1]   # checkbox vem depois do label no children (ordem reversa)
            lbl = children[i]
            if isinstance(cb, CheckBox) and isinstance(lbl, Label):
                checklist.append((lbl.text, cb.active))

        salvar_nota(
            self.id_atual, titulo, texto,
            self.cor_fundo, self.cor_texto, self.fonte,
            self.wallpaper, senha, anexos, checklist
        )
        self.manager.get_screen('principal').atualizar_lista()
        self.manager.current = 'principal'

    def deletar(self):
        if self.id_atual:
            deletar_nota(self.id_atual)
            self.manager.get_screen('principal').atualizar_lista()
        self.manager.current = 'principal'

    def adicionar_anexo(self):
        escolha = filechooser.open_file(title="Selecione PDF", filters=["*.pdf"])
        if escolha:
            caminho = escolha[0]
            self.anexos.append(caminho)
            self.ids.anexos_lista.text = "\n".join(self.anexos)

    def adicionar_checklist_item(self):
        texto = self.ids.novo_item.text.strip()
        if texto:
            cb = CheckBox(active=False, size_hint=(None, None), size=(48, 48))
            lbl = Label(text=texto, size_hint_y=None, height=48, valign='middle')
            self.ids.checklist.add_widget(lbl)
            self.ids.checklist.add_widget(cb)
            self.ids.novo_item.text = ""

    def atualizar_checklist(self, items):
        self.ids.checklist.clear_widgets()
        for texto, marcado in items:
            cb = CheckBox(active=marcado, size_hint=(None, None), size=(48, 48))
            lbl = Label(text=texto, size_hint_y=None, height=48, valign='middle')
            self.ids.checklist.add_widget(lbl)
            self.ids.checklist.add_widget(cb)

    def on_cor_fundo(self, *args):
        pass  # pode ser usado para atualizar canvas se quiser

    def on_cor_texto(self, *args):
        pass


class BlocoNotasApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("notas.kv")


if __name__ == '__main__':
    BlocoNotasApp().run()