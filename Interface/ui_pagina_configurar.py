import tkinter as t
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import re

# Mapeamento de nomes de unidade da UI para os do config.py
MAPA_UNIDADES_UI = {
    "KB - KiloBytes": "KB",
    "MB - MegaBytes": "MB",
    "GB - GigaBytes": "GB"
}
REVERSE_MAPA_UNIDADES_UI = {v: k for k, v in MAPA_UNIDADES_UI.items()}

class Tela_Configurar(t.Frame):

    def __init__(self, parent_frame, controller):
        super().__init__(parent_frame, background='#181f30', relief="flat", bd=0)
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
            self.label_background.image = self.background_image_tk # type: ignore
            self.label_background.grid(row=0, column=0, rowspan=8, columnspan=5, sticky="nsew")
            self.label_background.lower()

        except FileNotFoundError:
            print("Erro: Imagem 'Interface/Imagens/Página_Configurações_UI.png' não encontrada. Verifique o caminho.")
            messagebox.showerror("Erro de Arquivo", "A imagem de fundo 'Página_Configurações_UI.png' não foi encontrada. Verifique o caminho no código.")
            t.Label(self, text="Imagem não encontrada!", fg="red", bg="white").grid(row=0, column=0, rowspan=8, columnspan=5, sticky="nsew")


        mainframe = t.Frame(self, bg="white", relief="flat", bd=0)
        mainframe.place(x= 60, y= 125)

        for col in range(5):
            mainframe.columnconfigure(col, weight=0)
        for lin in range(9):
            mainframe.rowconfigure(lin, weight=0)

        # Variáveis de entrada de texto
        self.tam_mem_fis = t.StringVar()
        self.tam_mem_fis_entry = t.Entry(mainframe, width=20, textvariable=self.tam_mem_fis)
        self.tam_mem_fis_entry.grid(column= 1, row=2, sticky="we")
        t.Label(mainframe, text="Tamanho da Memória Física", bg= '#FFFFFF').grid(column= 1, row= 1, sticky= t.W)

        self.tam_mem_sec = t.StringVar()
        self.tam_mem_sec_entry = t.Entry(mainframe, width=20, textvariable=self.tam_mem_sec)
        self.tam_mem_sec_entry.grid(column= 1, row=5, sticky="we")
        t.Label(mainframe, text="Tamanho da Memória Secundária", bg= '#FFFFFF').grid(column= 1, row= 4, sticky= t.W)

        self.tam_pagina = t.StringVar()
        self.tam_pagina_entry = t.Entry(mainframe, width=20, textvariable=self.tam_pagina)
        self.tam_pagina_entry.grid(column= 1, row=8, sticky="we")
        t.Label(mainframe, text="Tamanho da Página e Quadro", bg= '#FFFFFF').grid(column= 1, row= 7, sticky= t.W)

        self.tam_end_log = t.StringVar()
        self.tam_end_log_entry = t.Entry(mainframe,width= 20, textvariable=self.tam_end_log)
        self.tam_end_log_entry.grid(column= 3, row= 2, sticky="we")
        t.Label(mainframe, text="Tamanho do Endereço Lógico (bits)", bg= '#FFFFFF').grid(column= 3, row= 1, sticky= t.W)

        self.num_lin_tlb = t.StringVar()
        self.num_lin_tlb_entry = t.Entry(mainframe, width= 20, textvariable=self.num_lin_tlb)
        self.num_lin_tlb_entry.grid(column= 3, row=5, sticky="we")
        t.Label(mainframe, text="Número de Linhas da TLB", bg= '#FFFFFF').grid(column= 3, row= 4, sticky= t.W)


        # --- COMBOBOX PARA UNIDADES DE MEMÓRIA ---
        self.unidade_memoriap_combobox = t.StringVar()
        self.unidade_memorias_combobox = t.StringVar()
        self.unidade_pagina_combobox = t.StringVar()

        self.combobox_unidade_memoriap = ttk.Combobox(
            mainframe, textvariable=self.unidade_memoriap_combobox,
            values=list(MAPA_UNIDADES_UI.keys()), state="readonly", width=15
        )
        self.combobox_unidade_memorias = ttk.Combobox(
            mainframe, textvariable=self.unidade_memorias_combobox,
            values=list(MAPA_UNIDADES_UI.keys()), state="readonly", width=15
        )
        self.combobox_unidade_pagina = ttk.Combobox(
            mainframe, textvariable=self.unidade_pagina_combobox,
            values=list(MAPA_UNIDADES_UI.keys()), state="readonly", width=15
        )
        
        # --- Posicionamento dos comboboxes ---
        self.combobox_unidade_memoriap.grid(column=1, row=3, sticky="we", padx=10, pady=2)
        self.combobox_unidade_memorias.grid(column=1, row=6, sticky="we", padx=10, pady=2)
        self.combobox_unidade_pagina.grid(column=1, row=9, sticky="we", padx=10, pady=2)
        
        # --- Botões ---
        t.Button(self, text="Voltar", command=lambda: controller.show_page("ui_pagina_inicial.py")).place(x=500, y=230)
        t.Button(self, text="Salvar", command=self.salvar_e_fechar).place(x=500, y=300)

        # Carrega as configurações atuais ao iniciar a tela
        self.carregar_configuracoes_atuais()

    def carregar_configuracoes_atuais(self):
        """
        Lê o arquivo config.py e preenche os campos da UI com os valores atuais.
        """
        try:
            with open("config.py", "r") as f:
                content = f.read()

            # Dicionário com as variáveis que queremos extrair e os widgets correspondentes
            mapa_config = {
                "TAMANHO_MEMORIA_PRINCIPAL_STR": (self.tam_mem_fis, self.unidade_memoriap_combobox),
                "TAMANHO_MEMORIA_SECUNDARIA_STR": (self.tam_mem_sec, self.unidade_memorias_combobox),
                "TAMANHO_PAGINA_QUADRO_STR": (self.tam_pagina, self.unidade_pagina_combobox),
                "TAMANHO_ENDERECO_LOGICO_BITS": self.tam_end_log,
                "NUMERO_LINHAS_TLB": self.num_lin_tlb,
            }

            for var_name, widgets in mapa_config.items():
                # Escolher o regex com base no tipo de widget esperado
                if isinstance(widgets, tuple):
                    # Para valores de string com unidade, ex: "64 KB"
                    regex = rf'^{var_name}\s*=\s*"([^"]+)"'
                else:
                    # Para valores numéricos simples, ex: 4
                    regex = rf'^{var_name}\s*=\s*(\d+)'
                
                match = re.search(regex, content, re.MULTILINE)
                if match:
                    valor = match.group(1).strip()
                    if isinstance(widgets, tuple):
                        # É uma configuração de tamanho com unidade (ex: "64 KB")
                        partes = valor.split()
                        if len(partes) == 2:
                            widgets[0].set(partes[0]) # Valor numérico
                            # Converte a unidade (KB) para a string da UI (KB - KiloBytes)
                            widgets[1].set(REVERSE_MAPA_UNIDADES_UI.get(partes[1].upper(), "KB - KiloBytes"))
                    else:
                        # É uma configuração numérica simples
                        widgets.set(valor)
        except FileNotFoundError:
            messagebox.showerror("Erro", "Arquivo de configuração 'config.py' não encontrado.")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar configurações: {e}")

    def salvar_e_fechar(self):
        """
        Valida os campos, salva as configurações e volta para a tela de input.
        """
        # --- Validação Simples na UI ---
        campos_para_validar = {
            "Tamanho da Memória Física": self.tam_mem_fis.get(),
            "Tamanho da Memória Secundária": self.tam_mem_sec.get(),
            "Tamanho da Página": self.tam_pagina.get(),
            "Endereço Lógico (bits)": self.tam_end_log.get(),
            "Linhas da TLB": self.num_lin_tlb.get()
        }
        for nome, valor in campos_para_validar.items():
            if not valor:
                messagebox.showerror("Erro de Validação", f"O campo '{nome}' não pode estar vazio.")
                return
            try:
                int(valor)
            except ValueError:
                messagebox.showerror("Erro de Validação", f"O campo '{nome}' deve conter um número inteiro.")
                return

        # Se a validação básica passar, tenta salvar.
        self.escrever_configuracoes()
        messagebox.showinfo("Sucesso", "Configurações salvas! O programa usará estas configurações na próxima simulação.")
        self.controller.show_page("ui_pagina_input.py")

    def escrever_configuracoes(self):
        """
        Pega as informações da UI e as escreve no arquivo config.py no formato correto.
        """
        # Constrói as strings de configuração no formato "VALOR UNIDADE"
        config_str_memp = f'"{self.tam_mem_fis.get()} {MAPA_UNIDADES_UI[self.unidade_memoriap_combobox.get()]}"'
        config_str_mems = f'"{self.tam_mem_sec.get()} {MAPA_UNIDADES_UI[self.unidade_memorias_combobox.get()]}"'
        config_str_pag = f'"{self.tam_pagina.get()} {MAPA_UNIDADES_UI[self.unidade_pagina_combobox.get()]}"'

        # Monta o dicionário de configurações com os nomes de variáveis do config.py
        novas_configs = {
            "TAMANHO_MEMORIA_PRINCIPAL_STR": config_str_memp,
            "TAMANHO_MEMORIA_SECUNDARIA_STR": config_str_mems,
            "TAMANHO_PAGINA_QUADRO_STR": config_str_pag,
            "TAMANHO_ENDERECO_LOGICO_BITS": self.tam_end_log.get(),
            "NUMERO_LINHAS_TLB": self.num_lin_tlb.get(),
        }

        try:
            with open("config.py", "r") as f:
                linhas = f.readlines()

            novas_linhas = []
            for linha in linhas:
                # Usa uma flag para ver se a linha foi substituída
                substituido = False
                for chave, valor in novas_configs.items():
                    if linha.strip().startswith(chave):
                        novas_linhas.append(f"{chave} = {valor}\n")
                        substituido = True
                        break
                if not substituido:
                    novas_linhas.append(linha)
            
            with open("config.py", "w") as f:
                f.writelines(novas_linhas)
            print("Arquivo config.py atualizado com sucesso pela UI.")

        except Exception as e:
            messagebox.showerror("Erro de Escrita", f"Não foi possível salvar as configurações: {e}")