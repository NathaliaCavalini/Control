import tkinter

tela = tkinter.Tk()
tela.title("Control") #Nome do software
tela.geometry("640x480") #Tamanho da tela

escrever_texto = tkinter.Text(tela, fonte="Arial 12")

iniciar_menu = tkinter.Menu(tela) #Menu principal

novo_menu = tkinter.Menu(iniciar_menu, tearoff=0) #Menu secundário

novo_menu.add_command(label="Novo")
novo_menu.add_command(label="Salvar")
novo_menu.add_command(label="Abrir")
novo_menu.add_command(label="Sair")

iniciar_menu.add_cascade(label="Arquivo", menu=novo_menu) #Como vai aparecer o menu
tela.config(menu=iniciar_menu)


tela.mainloop() #Deixar ela aberta por tempo indeterminado