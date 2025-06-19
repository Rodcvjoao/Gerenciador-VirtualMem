import tkinter as t
from tkinter import ttk
from PIL import Image, ImageTk 

class Tela_Configurar(t.Frame): 

    def __init__(self, parent_frame, controller):

        super().__init__(parent_frame, background='#181f30') 
        self.controller = controller

        style = ttk.Style()
        style.configure("Customize.TFrame", background="white")
        self.configure(background= '#181f30') 

        for col in range(5):
            self.columnconfigure(col, weight=1)
        for row in range(8):
            self.rowconfigure(row, weight=1)

        self.background_image_tk = None 
        try:
            imagem_fundo_pil = Image.open("Imagens/Página_Configurações_UI.png")
            self.background_image_tk = ImageTk.PhotoImage(imagem_fundo_pil)

            self.label_background = t.Label(self, image=self.background_image_tk, bg='#181f30')
            self.label_background.image = self.background_image_tk 
            self.label_background.grid(row=0, column=0, rowspan=8, columnspan=5, sticky="nsew") 
            self.label_background.lower() 

        except FileNotFoundError:
            print("Erro: Imagem 'Página Configurações.png' não encontrada.")
            t.Label(self, text="Imagem não encontrada!", fg="red", bg="white").grid(row=0, column=0, rowspan=8, columnspan=5, sticky="nsew")


        mainframe = ttk.Frame(self, style= "Customize.TFrame")
        mainframe.place(x= 60, y= 125)

        for col in range(5):
            mainframe.columnconfigure(col, weight=0)
        # Ajuste o range de linhas conforme necessário para o layout
        for lin in range(7): # Você pode ajustar para mais se precisar de mais linhas
            mainframe.rowconfigure(lin, weight=0)

        # Variáveis de entrada de texto
        self.tam_mem_fis = t.StringVar()
        tam_mem_fis_entry = t.Entry(mainframe, width=20, textvariable=self.tam_mem_fis)
        tam_mem_fis_entry.grid(column= 1, row=2, sticky=(t.W,t.E))
        t.Label(mainframe, text="Tamanho da Memória Física", bg= '#FFFFFF').grid(column= 1, row= 1, sticky= t.W)

        self.tam_mem_sec = t.StringVar()
        tam_mem_sec_entry = t.Entry(mainframe, width=20, textvariable=self.tam_mem_sec)
        tam_mem_sec_entry.grid(column= 1, row=5, sticky=(t.W,t.E))
        t.Label(mainframe, text="Tamanho da Memória Secundária", bg= '#FFFFFF').grid(column= 1, row= 4, sticky= t.W)

        self.tam_pagina = t.StringVar()
        tam_pagina_entry = t.Entry(mainframe, width=20, textvariable=self.tam_pagina)
        tam_pagina_entry.grid(column= 1, row=8, sticky=(t.W,t.E))
        t.Label(mainframe, text="Tamanho da Página do Processo", bg= '#FFFFFF').grid(column= 1, row= 7, sticky= t.W)

        self.tam_quad_mem = t.StringVar()
        tam_quad_mem_entry = t.Entry(mainframe, width=20, textvariable=self.tam_quad_mem)
        tam_quad_mem_entry.grid(column= 3, row=2, sticky=(t.W, t.E))
        t.Label(mainframe, text="Tamanho do Quadro de Memória", bg= '#FFFFFF').grid(column= 3, row= 1, sticky= t.W)

        self.tam_end_log = t.StringVar()
        tam_end_log_entry = t.Entry(mainframe,width= 20, textvariable=self.tam_end_log)
        tam_end_log_entry.grid(column= 3, row= 5, sticky=(t.W,t.E))
        t.Label(mainframe, text="Tamanho do Endereço Lógico", bg= '#FFFFFF').grid(column= 3, row= 4, sticky= t.W)

        self.num_lin_tlb = t.StringVar()
        num_lin_tlb_entry = t.Entry(mainframe, width= 20, textvariable=self.num_lin_tlb)
        num_lin_tlb_entry.grid(column= 3, row=8, sticky=(t.W,t.E))
        t.Label(mainframe, text="Número de Linhas da TLB", bg= '#FFFFFF').grid(column= 3, row= 7, sticky= t.W)


        # --- COMBOBOX PARA UNIDADES DE MEMÓRIA ---
        # Variável para armazenar a opção selecionada no Combobox
        self.unidade_memoriap_combobox = t.StringVar()
        self.unidade_memorias_combobox = t.StringVar()
        self.unidade_pagina_combobox = t.StringVar()
        self.unidade_quadro_combobox = t.StringVar()
        self.unidade_endlog_combobox = t.StringVar()



        # Define um valor inicial (opcional, pode ser uma das opções ou vazio)
        self.unidade_memoriap_combobox.set("KB - KiloBytes") 
        self.unidade_memorias_combobox.set("KB - KiloBytes") 
        self.unidade_pagina_combobox.set("KB - KiloBytes") 
        self.unidade_quadro_combobox.set("KB - KiloBytes") 
        self.unidade_endlog_combobox.set("KB - KiloBytes") 



        # Label para a seção de unidades de memória
        t.Label(mainframe, bg='#FFFFFF').grid(column=1, row=0, sticky=t.W, padx=10, pady=5)


        # Criação do Combobox
        combobox_unidade_memoriap = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_memoriap_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        combobox_unidade_memorias = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_memorias_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        combobox_unidade_pagina = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_pagina_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        combobox_unidade_quadro = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_quadro_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        combobox_unidade_endlog = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_endlog_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        combobox_unidade_memoriap.grid(column=1, row=3, sticky=(t.W, t.E), padx=10, pady=2)
        combobox_unidade_memorias.grid(column=1, row=6, sticky=(t.W, t.E), padx=10, pady=2)
        combobox_unidade_pagina.grid(column=1, row=9, sticky=(t.W, t.E), padx=10, pady=2)
        combobox_unidade_quadro.grid(column=3, row=3, sticky=(t.W, t.E), padx=10, pady=2)
        combobox_unidade_endlog.grid(column=3, row=6, sticky=(t.W, t.E), padx=10, pady=2)




        # Faz o espaçamento (após todos os widgets serem adicionados ao mainframe)
        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=6)

        # Botão para Voltar 
        t.Button(
            self, 
            text="Voltar",
            height=2,
            width=15,
            fg="white",
            bg="#0C0E8B",
            font=("monospace", 10, "bold"),
            activebackground= "#393CD1",
            command=lambda: self.controller.show_page("ui_pagina_inicial.py") 
        ).place(x= 500, y= 230) 

        #Botão Enviar
        t.Button(
            self, 
            text="Enviar",
            height=2,
            width=15,
            fg="white",
            bg="#1ECC6F",
            font=("monospace", 10, "bold"),
            command=lambda: self.controller.show_page("ui_pagina_input.py") 
        ).place(x= 500, y= 300)