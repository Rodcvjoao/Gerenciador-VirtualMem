import tkinter as t
from tkinter import ttk
from PIL import Image, ImageTk

class Tela_Inicial(t.Frame):

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

        # --- IMAGEM DE FUNDO ---
        try:
            imagem_fundo_pil = Image.open("Interface/Imagens/Página_Inicial_UI.png")
            self.background_image_tk = ImageTk.PhotoImage(imagem_fundo_pil)
            self.label_background = t.Label(self, image=self.background_image_tk, bg='#181f30')
            self.label_background.image = self.background_image_tk
            self.label_background.grid(row=0, column=0, rowspan=3, columnspan=5, sticky="nsew")
            self.label_background.lower()
        except FileNotFoundError:
            t.Label(self, text="Imagem 'Página Inicial UI.png' não encontrada.", fg="red", bg="white").grid(row=0, column=0, rowspan=3, columnspan=5, sticky="nsew")

    
        auxiliar_botao = t.Frame(self, bg="white", relief="flat", bd=0)
        auxiliar_botao.grid(column= 1, row= 1, columnspan=5, sticky= "w")

        for col in range(5):
            auxiliar_botao.columnconfigure(col, weight=0)

        auxiliar_botao.columnconfigure(0, weight=0)
        auxiliar_botao.columnconfigure(1, weight=0)
        auxiliar_botao.columnconfigure(2, weight=0)
        auxiliar_botao.columnconfigure(3, weight=0)
        auxiliar_botao.columnconfigure(4, weight=0)
        
        t.Button(
            auxiliar_botao,
            text="Configurar o Gerenciador", 
            height=2,
            width=30,
            fg="#FFFFFF",
            bg="#0C0E8B",
            relief="flat",           
            bd=0,                   
            highlightthickness=0,
            font=("monospace", 12, "bold"),
            command=lambda: self.controller.show_page("ui_pagina_configurar.py"),
            activebackground="#393CD1",
            activeforeground="#FFFFFF",
        ).pack(padx=20, pady=20)