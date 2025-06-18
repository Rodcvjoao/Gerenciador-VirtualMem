import tkinter as t
from tkinter import ttk
from PIL import Image, ImageTk


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
            imagem_fundo_pil = Image.open("Imagens/Página_Input_UI.png")
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
        auxiliar_botao.grid(column= 3, row= 1, columnspan=5, sticky= "w")

        for col in range(5):
            auxiliar_botao.columnconfigure(col, weight=0)

        auxiliar_botao.columnconfigure(0, weight=0)
        auxiliar_botao.columnconfigure(1, weight=0)
        auxiliar_botao.columnconfigure(2, weight=0)
        auxiliar_botao.columnconfigure(3, weight=0)
        auxiliar_botao.columnconfigure(4, weight=0)


        # Inserção de Botão Enviar
        t.Button(
            auxiliar_botao,
            text="Enviar",
            height=2,
            width=30,
            fg="#FFFFFF",
            bg="#0C0E8B",
            font=("monospace", 12, "bold"),
            command=lambda: self.controller.show_page("ui_pagina_simular.py"),
            activebackground="#393CD1", # Cor de fundo ao clicar (um azul um pouco mais escuro)
            activeforeground="#FFFFFF", # Cor do texto ao clicar (um cinza claro)
        ).grid(column=0, row=0, sticky="ew", padx=5)