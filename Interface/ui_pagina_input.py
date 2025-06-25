
import tkinter as t
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import re

class Tela_Input(t.Frame):

    def __init__(self,parent_frame,controller):
        super().__init__(parent_frame)
        self.controller = controller
        self.configure(background='#181f30')
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- IMAGEM DE FUNDO ---
        try:
            imagem_fundo_pil = Image.open("Interface/Imagens/Página_Input_UI.png")
            self.background_image_tk = ImageTk.PhotoImage(imagem_fundo_pil)
            label_background = t.Label(self, image=self.background_image_tk, bg='#181f30')
            label_background.image = self.background_image_tk
            # Usando place para a imagem de fundo, pois ela não interfere com outros widgets
            label_background.place(x=0, y=0, relwidth=1, relheight=1)
            label_background.lower()
        except FileNotFoundError:
            # Em caso de erro, um label simples para não quebrar o layout
            t.Label(self, text="Imagem de fundo não encontrada", fg="red", bg="#181f30").grid(row=0, column=0)


        content_frame = t.Frame(self, bg="white", padx=20, pady=20, relief="groove", borderwidth=2)
        content_frame.grid(row=1, column=0, sticky="") # sticky="" centraliza

        # --- WIDGETS DENTRO DO FRAME CENTRAL (usando pack) ---
        t.Label(content_frame, text="Digite ou selecione o arquivo de teste:", bg="white", font=("monospace", 12)).pack(pady=10, padx=10)

        self.entrada = t.StringVar()
        self.entrada_entry = t.Entry(content_frame, width=50, textvariable=self.entrada, font=("monospace", 11))
        self.entrada_entry.pack(pady=10, padx=10)

        t.Button(
            content_frame,
            text="Procurar Arquivo...",
            command=self.procurar_arquivo,
            bg="#d0d0d0",
            font=("monospace", 10),
            padx=10, pady=5
        ).pack(pady=10)

        # --- FRAME PARA OS BOTÕES DE NAVEGAÇÃO ---
        # Este frame será posicionado na linha 2, coluna 0 do grid principal
        botoes_frame = t.Frame(self, bg='#181f30')
        botoes_frame.grid(row=2, column=0, pady=20)

        t.Button(
            botoes_frame,
            text="Voltar",
            height=2, width=15, fg="#FFFFFF", bg="#0C0E8B", font=("monospace", 11, "bold"),
            command=lambda: self.controller.show_page("ui_pagina_inicial.py"),
        ).pack(side=t.LEFT, padx=20)

        t.Button(
            botoes_frame,
            text="Simular",
            height=2, width=15, fg="#FFFFFF", bg="#1ECC6F", font=("monospace", 11, "bold"),
            command=self.salvar_e_simular,
        ).pack(side=t.LEFT, padx=20)


    def procurar_arquivo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o arquivo de teste",
            filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        if caminho:
            self.entrada.set(caminho)

    def salvar_e_simular(self):
        caminho = self.entrada.get()
        if not caminho:
            messagebox.showwarning("Campo Vazio", "Por favor, digite ou selecione um arquivo de teste antes de simular.")
            return

        
        
        self.controller.show_page("ui_pagina_simular.py")
        pagina_simular = self.controller.get_page("ui_pagina_simular.py")
        pagina_simular.rodar_e_mostrar_simulacao(caminho) # Passa o caminho como argumento