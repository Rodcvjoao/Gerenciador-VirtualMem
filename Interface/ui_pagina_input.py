import tkinter as t
from tkinter import ttk
from PIL import Image, ImageTk
import re

class Tela_Input(t.Frame):

    def __init__(self,parent_frame,controller):

        super().__init__(parent_frame)
        self.controller = controller

        style = ttk.Style()
        style.configure("Custom.TFrame", background="white")
        self.configure(background= '#181f30') 

        for col in range(5):
            self.columnconfigure(col, weight=1)
        for row in range(3):
            self.rowconfigure(row, weight=1)

        # --- IMAGEM DE FUNDO FIXA QUE PREENCHE O FRAME ---
        self.background_image_tk = None 
        try:
            imagem_fundo_pil = Image.open("Interface/Imagens/Página_Input_UI.png")
            self.background_image_tk = ImageTk.PhotoImage(imagem_fundo_pil)

            # Criar um Label para exibir a imagem
            self.label_background = t.Label(self, image=self.background_image_tk, bg='#181f30')
            self.label_background.image = self.background_image_tk # Manter a referência
            
            # Posicionar o Label da imagem para preencher o Tela_Inicial frame
            # Ele estará na camada de baixo
            self.label_background.grid(row=0, column=0, rowspan=3, columnspan=5, sticky="nsew")
            self.label_background.lower() # Garante que fique no fundo, abaixo de outros widgets


        except FileNotFoundError:
            print("Erro: Imagem 'Página Input UI.png' não encontrada.")
            # Se a imagem não for encontrada, exibe um Label de erro centralizado
            t.Label(self, text="Imagem não encontrada!", fg="red", bg="white").grid(row=0, column=0, rowspan=3, columnspan=5, sticky="nsew")


        # --- RESTANTE DOS SEUS WIDGETS (EXATAMENTE COMO ESTAVAM) ---
        # O auxiliar_botao e o botão dentro dele manterão seu posicionamento original
        # mas agora aparecerão acima do label_background
        auxiliar_botao = ttk.Frame(self, style= "Custom.TFrame")
        auxiliar_botao.grid(column= 3, row= 2, columnspan=5, sticky= "w")

        for col in range(5):
            auxiliar_botao.columnconfigure(col, weight=0)
        
        for lin in range(5):
            auxiliar_botao.rowconfigure(row, weight=0)

        m = t.Frame(self)
        m.place(x= 210, y= 240)

        for col in range(10):
            m.columnconfigure(col, weight=0)
        # Ajuste o range de linhas conforme necessário para o layout
        for lin in range(10): # Você pode ajustar para mais se precisar de mais linhas
            m.rowconfigure(lin, weight=0)

        self.entrada = t.StringVar()
        self.entrada_entry = t.Entry(m, width=40, textvariable=self.entrada)
        self.entrada_entry.grid(row=3, column = 4,sticky=(t.W,t.E))
        t.Label(m, bg= '#FFFFFF').place(x= 210, y= 240)


        # Inserção de Botão Enviar
        t.Button(
            auxiliar_botao,
            text="Enviar",
            height=2,
            width=20,
            fg="#FFFFFF",
            bg="#1ECC6F",
            font=("monospace", 12, "bold"),
            command= self.salvar_config,
            activebackground="#696969", # 
            activeforeground="#FFFFFF", # Cor do texto ao clicar (um cinza claro)
        ).grid(row= 2, column= 4, sticky= "ew")


        auxiliar_botao2 = ttk.Frame(self, style= "Custom.TFrame")
        auxiliar_botao2.grid(column= 1, row= 2, columnspan=5, sticky= "w")

        for col in range(5):
            auxiliar_botao2.columnconfigure(col, weight=0)
        
        for lin in range(5):
            auxiliar_botao2.rowconfigure(row, weight=0)


        # Inserção de Botão Voltar
        t.Button(
            auxiliar_botao2,
            text="Voltar",
            height=2,
            width=20,
            fg="#FFFFFF",
            bg="#0C0E8B",
            font=("monospace", 12, "bold"),
            command=lambda: self.controller.show_page("ui_pagina_configurar.py"),
            activebackground="#393CD1", # Cor de fundo ao clicar (um azul um pouco mais escuro)
            activeforeground="#FFFFFF", # Cor do texto ao clicar (um cinza claro)
        ).grid(row= 0, column= 1, sticky= "ew")

    def salvar_config(self):

        self.pegar_arquivo_teste()  # Chama o método que coleta e salva as informações
        self.controller.show_page("ui_pagina_simular.py") # Navega para a próxima página
        

    def pegar_arquivo_teste(self):

        caminho = self.entrada_entry.get()

        # Lê o conteúdo atual
        try:
            with open("config.py", "r") as arquivo:
                linhas = arquivo.readlines()
        except FileNotFoundError:
            print("Erro: O arquivo não foi encontrado. Criando um novo.")
            linhas = [] # Começa com uma lista vazia se o arquivo não existir
        
        # Lista de variáveis que queremos salvar
        novas_configs = {
            "ARQ_TESTE": f'"{caminho}"',
        }

        # Atualiza ou adiciona as variáveis
        novas_linhas = []
        for linha in linhas:
            atualizado = False
            for chave, valor in novas_configs.items():
                padrao = re.compile(rf"^{chave}\s*=")
                if padrao.match(linha):
                    novas_linhas.append(f"{chave} = {valor}\n")
                    atualizado = True
                    break
            if not atualizado:
                novas_linhas.append(linha)


        # Regrava o arquivo
        try:
            with open("config.py","w") as arquivo:
                arquivo.writelines(novas_linhas)
            print("Configuração salva/atualizada em: config.py")
        except IOError as e:
            print(f"Erro ao escrever no arquivo 'config.py': {e}")