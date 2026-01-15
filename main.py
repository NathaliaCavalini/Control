import tkinter

def novo_arquivo():
    escrever_texto.delete(1.0, "end")

def salvar_arquivo():
    container = escrever_texto.get(1.0, "end")
    with open("teste.txt", "w") as arquivo:
        arquivo.write(container)

def abrir_arquivo():
    with open("teste.txt", "r") as arquivo:
        mostrar = arquivo.read()
        escrever_texto.insert(1.0, mostrar)



tela = tkinter.Tk()
tela.title("Control") #Nome do software
tela.geometry("640x480") #Tamanho da tela

escrever_texto = tkinter.Text(tela, font="Arial 12")
escrever_texto.pack()

iniciar_menu = tkinter.Menu(tela) #Menu principal

novo_menu = tkinter.Menu(iniciar_menu, tearoff=0) #Menu secundário

novo_menu.add_command(label="Novo", command=novo_arquivo)
novo_menu.add_command(label="Salvar", command=salvar_arquivo)
novo_menu.add_command(label="Abrir", command=abrir_arquivo)
novo_menu.add_command(label="Sair", command=tela.quit)

iniciar_menu.add_cascade(label="Arquivo", menu=novo_menu) #Como vai aparecer o menu
tela.config(menu=iniciar_menu)


tela.mainloop() #Deixar ela aberta por tempo indeterminado