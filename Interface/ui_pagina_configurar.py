import tkinter as t
from tkinter import ttk, messagebox
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
            print("Erro: Imagem 'Interface/Imagens/Página_Configurações_UI.png' não encontrada. Verifique o caminho.")
            messagebox.showerror("Erro de Arquivo", "A imagem de fundo 'Página_Configurações_UI.png' não foi encontrada. Verifique o caminho no código.")
            t.Label(self, text="Imagem não encontrada!", fg="red", bg="white").grid(row=0, column=0, rowspan=8, columnspan=5, sticky="nsew")


        mainframe = ttk.Frame(self, style= "Customize.TFrame")
        mainframe.place(x= 60, y= 125)

        for col in range(5):
            mainframe.columnconfigure(col, weight=0)
        for lin in range(9):
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
        t.Label(mainframe, text="Tamanho da Página e Quadro do Processo", bg= '#FFFFFF').grid(column= 1, row= 7, sticky= t.W)

        self.tam_end_log = t.StringVar()
        self.tam_end_log_entry = t.Entry(mainframe,width= 20, textvariable=self.tam_end_log)
        self.tam_end_log_entry.grid(column= 3, row= 2, sticky=(t.W,t.E))
        t.Label(mainframe, text="Tamanho do Endereço Lógico", bg= '#FFFFFF').grid(column= 3, row= 1, sticky= t.W)

        self.num_lin_tlb = t.StringVar()
        self.num_lin_tlb_entry = t.Entry(mainframe, width= 20, textvariable=self.num_lin_tlb)
        self.num_lin_tlb_entry.grid(column= 3, row=5, sticky=(t.W,t.E))
        t.Label(mainframe, text="Número de Linhas da TLB", bg= '#FFFFFF').grid(column= 3, row= 4, sticky= t.W)


        # --- COMBOBOX PARA UNIDADES DE MEMÓRIA ---
        self.unidade_memoriap_combobox = t.StringVar()
        self.unidade_memorias_combobox = t.StringVar()
        self.unidade_pagina_combobox = t.StringVar()
        self.unidade_endlog_combobox = t.StringVar()


        self.unidade_memoriap_combobox.set("KB - KiloBytes")
        self.unidade_memorias_combobox.set("KB - KiloBytes")
        self.unidade_pagina_combobox.set("KB - KiloBytes")


        t.Label(mainframe, bg='#FFFFFF').grid(column=1, row=0, sticky=t.W, padx=10, pady=5)


        # Criação do Combobox
        self.combobox_unidade_memoriap = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_memoriap_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly",
            width=15
        )

        self.combobox_unidade_memorias = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_memorias_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly",
            width=15
        )

        self.combobox_unidade_pagina = ttk.Combobox(
            mainframe,
            textvariable=self.unidade_pagina_combobox,
            values=["KB - KiloBytes", "MB - MegaBytes", "GB - GigaBytes"],
            state="readonly",
            width=15
        )


        self.combobox_unidade_memoriap.grid(column=1, row=3, sticky=(t.W, t.E), padx=10, pady=2)
        self.combobox_unidade_memorias.grid(column=1, row=6, sticky=(t.W, t.E), padx=10, pady=2)
        self.combobox_unidade_pagina.grid(column=1, row=9, sticky=(t.W, t.E), padx=10, pady=2)


        for child in mainframe.winfo_children():
            child.grid_configure(padx=10, pady=6)

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

    # Função auxiliar para verificar se um número é potência de 2 (EXATAMENTE COMO FORNECIDO)
    def ehPotenciaDeDois(self, n):
        try:
            n_int = int(n)
        except ValueError: # Caso a entrada não seja um número inteiro
            return False
        if n_int <= 0:
            return False
        return (n_int & (n_int - 1)) == 0

    def salvar_configuracoes(self):
        # Mapeamento das entradas e seus nomes para mensagens de erro
        # Primeiro, obtenha todos os valores para poder fazer validações cruzadas
        valor_tam_mem_fis_str = self.tam_mem_fis_entry.get()
        valor_tam_mem_sec_str = self.tam_mem_sec_entry.get()
        valor_tam_pagina_str = self.tam_pagina_entry.get()
        valor_tam_end_log_str = self.tam_end_log_entry.get()
        valor_num_lin_tlb_str = self.num_lin_tlb_entry.get()

        # Dicionário para armazenar os valores convertidos para uso nas validações
        # e evitar múltiplas conversões ou erros por tipo
        valores_numericos = {}

        # Função auxiliar para validar e converter para int
        def get_and_validate_int(campo_nome, valor_str):
            if not valor_str:
                messagebox.showerror("Erro de Validação", f"O campo '{campo_nome}' não pode estar vazio.")
                return None
            try:
                valor = int(valor_str)
                return valor
            except ValueError:
                messagebox.showerror("Erro de Validação", f"O valor para '{campo_nome}' deve ser um número inteiro.")
                return None

        # Validação inicial de tipo e vazio para todos os campos numéricos
        valores_numericos['NUM_LINHAS_TLB'] = get_and_validate_int("Número de Linhas da TLB", valor_num_lin_tlb_str)
        valores_numericos['TAM_PAGINA_QUADRO'] = get_and_validate_int("Tamanho da Página do Processo", valor_tam_pagina_str)
        valores_numericos['TAM_MEMORIA_P'] = get_and_validate_int("Tamanho da Memória Física", valor_tam_mem_fis_str)
        valores_numericos['TAM_MEMORIA_S'] = get_and_validate_int("Tamanho da Memória Secundária", valor_tam_mem_sec_str)
        valores_numericos['TAM_END_LOGICO'] = get_and_validate_int("Tamanho do Endereço Lógico", valor_tam_end_log_str)

        # Se algum campo não passou na validação inicial (tipo ou vazio), get_and_validate_int já mostrou erro
        # e retornou None, então podemos parar aqui.
        if any(v is None for v in valores_numericos.values()):
            return

        # Aplicação das regras de validação específicas (agora com valores numéricos)
        # NUMERO_LINHAS_TLB
        if valores_numericos['NUM_LINHAS_TLB'] <= 0:
            messagebox.showerror("Erro de Validação", "ERRO: Número de Linhas da TLB deve ser maior que zero.")
            return

        # TAMANHO_PAGINA
        if valores_numericos['TAM_PAGINA_QUADRO'] <= 0 or not self.ehPotenciaDeDois(valores_numericos['TAM_PAGINA_QUADRO']):
            messagebox.showerror("Erro de Validação", "ERRO: Tamanho da Página do Processo deve ser maior que zero e potência de 2.")
            return

        # TAMANHO_MEMORIA_P (Memória Física)
        if valores_numericos['TAM_MEMORIA_P'] <= 0 or \
           valores_numericos['TAM_MEMORIA_P'] < valores_numericos['TAM_PAGINA_QUADRO'] or \
           not self.ehPotenciaDeDois(valores_numericos['TAM_MEMORIA_P']):
            messagebox.showerror("Erro de Validação", "ERRO: Tamanho da Memória Física deve ser maior que zero, maior ou igual ao Tamanho da Página do Processo e potência de 2.")
            return
            
        # Adicionando validação para os outros campos 
        # TAM_MEM_SECUNDARIA
        if valores_numericos['TAM_MEMORIA_S'] <= 0 or not self.ehPotenciaDeDois(valores_numericos['TAM_MEMORIA_S']):
            messagebox.showerror("Erro de Validação", "ERRO: Tamanho da Memória Secundária deve ser maior que zero e potência de 2.")
            return

        
        # TAM_END_LOGICO
        if valores_numericos['TAM_END_LOGICO'] <= 0 or not self.ehPotenciaDeDois(valores_numericos['TAM_END_LOGICO']):
            messagebox.showerror("Erro de Validação", "ERRO: Tamanho do Endereço Lógico deve ser maior que zero e potência de 2.")
            return


        # Se todas as validações passarem, prossegue com a coleta e salvamento das informações
        self.pegar_info()
        messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")
        self.controller.show_page("ui_pagina_input.py")


    # Leva as informações da interface para config
    def pegar_info(self):
        # Coleta os valores (já validados como strings, mas que representam números)
        info_tam_memp = self.tam_mem_fis_entry.get()
        info_tam_mems = self.tam_mem_sec_entry.get()
        info_tam_pag = self.tam_pagina_entry.get()
        info_tam_endlog = self.tam_end_log_entry.get()
        info_num_lin_tlb = self.num_lin_tlb_entry.get()

        info_unidade_memp = self.combobox_unidade_memoriap.get()
        info_unidade_mems = self.combobox_unidade_memorias.get()
        info_unidade_pag = self.combobox_unidade_pagina.get()

        try:
            with open("config.py", "r") as arquivo:
                linhas = arquivo.readlines()
        except FileNotFoundError:
            print("Aviso: O arquivo 'config.py' não foi encontrado. Criando um novo.")
            linhas = []


        novas_configs = {
            "TAM_MEM_PRINCIPAL": info_tam_memp,
            "TAM_MEM_SECUNDARIA": info_tam_mems,
            "TAM_PAGINA_QUADRO": info_tam_pag,
            "TAM_END_LOGICO": info_tam_endlog,
            "NUM_LINHAS_TLB": info_num_lin_tlb,
            "UNID_MEMP" : info_unidade_memp,
            "UNID_MEMS" : info_unidade_mems,
            "UNID_PAG_QUAD" : info_unidade_pag,
        }

        novas_linhas_conteudo = []
        chaves_encontradas = set()

        for linha in linhas:
            atualizado = False
            for chave, valor in novas_configs.items():
                padrao = re.compile(rf"^{chave}\s*=")
                if padrao.match(linha):
                    novas_linhas_conteudo.append(f"{chave} = \"{valor}\"\n")
                    atualizado = True
                    chaves_encontradas.add(chave)
                    break
            if not atualizado:
                novas_linhas_conteudo.append(linha)

        for chave, valor in novas_configs.items():
            if chave not in chaves_encontradas:
                novas_linhas_conteudo.append(f"{chave} = \"{valor}\"\n")

        try:
            with open("config.py","w") as arquivo:
                arquivo.writelines(novas_linhas_conteudo)
            print("Configuração salva/atualizada em: config.py")
        except IOError as e:
            print(f"Erro ao escrever no arquivo 'config.py': {e}")
            messagebox.showerror("Erro de Escrita", f"Não foi possível salvar as configurações no arquivo 'config.py': {e}")