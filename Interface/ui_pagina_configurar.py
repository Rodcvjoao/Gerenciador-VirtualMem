import tkinter as t
from tkinter import ttk
from PIL import Image, ImageTk 
import re

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
            imagem_fundo_pil = Image.open("Interface/Imagens/Página_Configurações_UI.png")
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
        self.tam_mem_fis_entry = t.Entry(mainframe, width=20, textvariable=self.tam_mem_fis)
        self.tam_mem_fis_entry.grid(column= 1, row=2, sticky=(t.W,t.E))
        t.Label(mainframe, text="Tamanho da Memória Física", bg= '#FFFFFF').grid(column= 1, row= 1, sticky= t.W)

        self.tam_mem_sec = t.StringVar()
        self.tam_mem_sec_entry = t.Entry(mainframe, width=20, textvariable=self.tam_mem_sec)
        self.tam_mem_sec_entry.grid(column= 1, row=5, sticky=(t.W,t.E))
        t.Label(mainframe, text="Tamanho da Memória Secundária", bg= '#FFFFFF').grid(column= 1, row= 4, sticky= t.W)

        self.tam_pagina = t.StringVar()
        self.tam_pagina_entry = t.Entry(mainframe, width=20, textvariable=self.tam_pagina)
        self.tam_pagina_entry.grid(column= 1, row=8, sticky=(t.W,t.E))
        t.Label(mainframe, text="Tamanho da Página do Processo", bg= '#FFFFFF').grid(column= 1, row= 7, sticky= t.W)

        self.tam_quad_mem = t.StringVar()
        self.tam_quad_mem_entry = t.Entry(mainframe, width=20, textvariable=self.tam_quad_mem)
        self.tam_quad_mem_entry.grid(column= 3, row=2, sticky=(t.W, t.E))
        t.Label(mainframe, text="Tamanho do Quadro de Memória", bg= '#FFFFFF').grid(column= 3, row= 1, sticky= t.W)

        self.tam_end_log = t.StringVar()
        self.tam_end_log_entry = t.Entry(mainframe,width= 20, textvariable=self.tam_end_log)
        self.tam_end_log_entry.grid(column= 3, row= 5, sticky=(t.W,t.E))
        t.Label(mainframe, text="Tamanho do Endereço Lógico", bg= '#FFFFFF').grid(column= 3, row= 4, sticky= t.W)

        self.num_lin_tlb = t.StringVar()
        self.num_lin_tlb_entry = t.Entry(mainframe, width= 20, textvariable=self.num_lin_tlb)
        self.num_lin_tlb_entry.grid(column= 3, row=8, sticky=(t.W,t.E))
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
        self.combobox_unidade_memoriap = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_memoriap_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        self.combobox_unidade_memorias = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_memorias_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        self.combobox_unidade_pagina = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_pagina_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        self.combobox_unidade_quadro = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_quadro_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        self.combobox_unidade_endlog = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_endlog_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly", # Impede que o usuário digite valores personalizados
            width=15 # Ajuste a largura conforme necessário
        )

        self.combobox_unidade_memoriap.grid(column=1, row=3, sticky=(t.W, t.E), padx=10, pady=2)
        self.combobox_unidade_memorias.grid(column=1, row=6, sticky=(t.W, t.E), padx=10, pady=2)
        self.combobox_unidade_pagina.grid(column=1, row=9, sticky=(t.W, t.E), padx=10, pady=2)
        self.combobox_unidade_quadro.grid(column=3, row=3, sticky=(t.W, t.E), padx=10, pady=2)
        self.combobox_unidade_endlog.grid(column=3, row=6, sticky=(t.W, t.E), padx=10, pady=2)


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
            command=self.salvar_configuracoes, 
            activebackground="#696969"
        ).place(x= 500, y= 300)


    def salvar_configuracoes(self):

        self.pegar_info()  # Chama o método que coleta e salva as informações
        self.controller.show_page("ui_pagina_input.py") # Navega para a próxima página


    # Leva as informações da interface para config
    def pegar_info(self):

        info_tam_memp = self.tam_mem_fis_entry.get()
        info_tam_mems = self.tam_mem_sec_entry.get()
        info_tam_pag = self.tam_pagina_entry.get()
        info_tam_quadro = self.tam_quad_mem_entry.get()
        info_tam_endlog = self.tam_end_log_entry.get()
        info_num_lin_tlb = self.num_lin_tlb_entry.get()

        info_unidade_memp = self.combobox_unidade_memoriap.get()
        info_unidade_mems = self.combobox_unidade_memorias.get()
        info_unidade_pag = self.combobox_unidade_pagina.get()
        info_unidade_quadro = self.combobox_unidade_quadro.get()
        info_unidade_endlog = self.combobox_unidade_endlog.get()


        # Lê o conteúdo atual
        try:
            with open("config.py", "r") as arquivo:
                linhas = arquivo.readlines()
        except FileNotFoundError:
            print("Erro: O arquivo 'config.py' não foi encontrado. Criando um novo.")
            linhas = [] # Começa com uma lista vazia se o arquivo não existir


        # Lista de variáveis que queremos salvar
        novas_configs = {
            "TAM_MEM_PRINCIPAL": f'"{info_tam_memp}"',
            "TAM_MEM_SECUNDARIA": f'"{info_tam_mems}"',
            "TAM_PAGINA": f'"{info_tam_pag}"',
            "TAM_QUADRO": f'"{info_tam_quadro}"',
            "TAM_END_LOGICO": f'"{info_tam_endlog}"',
            "NUM_LINHAS_TLB": f'"{info_num_lin_tlb}"',
            "UNID_MEMP" : f'"{info_unidade_memp}"',
            "UNID_MEMS" : f'"{info_unidade_mems}"',
            "UNID_PAG" : f'"{info_unidade_pag}"',
            "UNID_QUAD" : f'"{info_unidade_quadro}"',
            "UNID_ENDLOG" : f'"{info_unidade_endlog}"',

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