import tkinter as tk
from tkinter import ttk, messagebox
import re
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memoriaPrincipal import MemoriaPrincipal
from config import (
    ARQ_TESTE, TAM_MEM_PRINCIPAL, TAM_PAGINA_QUADRO,
    NUM_LINHAS_TLB, POLITICA_SUBST, MAPA_UNIDADES
)
from tlb import TLB
from classesProcessos import Processo
from main import tratar_acesso_memoria


class Tela_Simular(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#181f30')
        
        # Configurar tamanho fixo da janela
        if parent.winfo_toplevel():
            parent.winfo_toplevel().geometry('700x500')
            parent.winfo_toplevel().resizable(False, False)
        
        # Variáveis da simulação
        self.mp: MemoriaPrincipal | None = None
        self.tlb: TLB | None = None
        self.processos_lista: list[Processo] = []
        self.comandos: list[tuple] = []
        self.ciclo_atual = 0
        self.simulacao_iniciada = False
        
        # Criar interface
        self.criar_interface()
        
    def criar_interface(self):
        """Cria todos os elementos da interface para tela 700x500"""
        # Frame principal com tamanho fixo
        main_frame = tk.Frame(self, bg='#181f30', width=700, height=500)
        main_frame.pack_propagate(False)  # Impede redimensionamento automático
        main_frame.pack(fill='both', expand=True)
        
        # Header compacto (60px)
        header_frame = tk.Frame(main_frame, bg='#181f30', height=60)
        header_frame.pack(fill='x', padx=5, pady=2)
        header_frame.pack_propagate(False)
        
        # Título e controles na mesma linha
        tk.Label(header_frame, text="Simulador de Memória Virtual", 
                font=('Arial', 14, 'bold'), bg='#181f30', fg='white').pack(side='left', pady=5)
        
        # Controles à direita
        controles_frame = tk.Frame(header_frame, bg='#181f30')
        controles_frame.pack(side='right', pady=5)
        
        btn_iniciar = tk.Button(controles_frame, text="Iniciar", 
                               command=self.iniciar_simulacao,
                               font=('Arial', 9), bg='#38a169', fg='white',
                               relief='flat', padx=10, pady=4)
        btn_iniciar.pack(side='left', padx=2)
        
        btn_reset = tk.Button(controles_frame, text="Reset", 
                            command=self.reset_simulacao,
                            font=('Arial', 9), bg='#e53e3e', fg='white',
                            relief='flat', padx=10, pady=4)
        btn_reset.pack(side='left', padx=2)
        
        # Info do ciclo
        info_frame = tk.Frame(header_frame, bg='#181f30')
        info_frame.pack(side='right', padx=10)
        
        self.label_ciclo = tk.Label(info_frame, text=f"Ciclo: {self.ciclo_atual}", 
                                   font=('Arial', 11, 'bold'), bg='#181f30', fg='white')
        self.label_ciclo.pack()
        
        # Estatísticas em linha horizontal (30px)
        stats_frame = tk.Frame(main_frame, bg='#2d3748', height=30)
        stats_frame.pack(fill='x', padx=5, pady=2)
        stats_frame.pack_propagate(False)
        
        tk.Label(stats_frame, text="Estatísticas TLB:", font=('Arial', 9, 'bold'), 
                bg='#2d3748', fg='white').pack(side='left', padx=5)
        
        self.label_acertos = tk.Label(stats_frame, text="Acertos: 0", font=('Arial', 9), 
                                     bg='#2d3748', fg='#68d391')
        self.label_acertos.pack(side='left', padx=10)
        
        self.label_falhas = tk.Label(stats_frame, text="Falhas: 0", font=('Arial', 9), 
                                    bg='#2d3748', fg='#f56565')
        self.label_falhas.pack(side='left', padx=10)
        
        self.label_taxa = tk.Label(stats_frame, text="Taxa: 0%", font=('Arial', 9), 
                                  bg='#2d3748', fg='#63b3ed')
        self.label_taxa.pack(side='left', padx=10)
        
        # Controles de navegação na mesma linha das estatísticas
        nav_frame = tk.Frame(stats_frame, bg='#2d3748')
        nav_frame.pack(side='right', padx=5)
        
        self.btn_voltar = tk.Button(nav_frame, text="◀", command=self.voltar_ciclo,
                                   font=('Arial', 8, 'bold'), bg='#4299e1', fg='white',
                                   width=3, relief='flat', state='disabled')
        self.btn_voltar.pack(side='left', padx=1)
        
        self.btn_proximo = tk.Button(nav_frame, text="▶", command=self.executar_proximo_ciclo,
                                    font=('Arial', 8, 'bold'), bg='#38a169', fg='white',
                                    width=3, relief='flat', state='disabled')
        self.btn_proximo.pack(side='left', padx=1)
        
        # Área principal das tabelas (360px)
        tabelas_frame = tk.Frame(main_frame, bg='#181f30', height=360)
        tabelas_frame.pack(fill='both', expand=True, padx=5, pady=2)
        tabelas_frame.pack_propagate(False)
        
        # Dividir em duas colunas
        # Coluna esquerda (340px)
        left_frame = tk.Frame(tabelas_frame, bg='#181f30', width=340)
        left_frame.pack(side='left', fill='y', padx=(0, 2))
        left_frame.pack_propagate(False)
        
        # TLB (180px)
        self.criar_tabela_tlb(left_frame, height=180)
        
        # Processos Ativos (175px)
        self.criar_tabela_processos(left_frame, height=175)
        
        # Coluna direita (340px)
        right_frame = tk.Frame(tabelas_frame, bg='#181f30', width=340)
        right_frame.pack(side='right', fill='y', padx=(2, 0))
        right_frame.pack_propagate(False)
        
        # Memória Principal (180px)
        self.criar_tabela_memoria_principal(right_frame, height=180)
        
        # Memória Secundária (175px)
        self.criar_tabela_memoria_secundaria(right_frame, height=175)
        
        # Footer compacto (40px)
        footer_frame = tk.Frame(main_frame, bg='#181f30', height=40)
        footer_frame.pack(fill='x', padx=5, pady=2)
        footer_frame.pack_propagate(False)
        
        # Status
        self.label_status = tk.Label(footer_frame, text="Status: Aguardando início", 
                                    font=('Arial', 9), bg='#181f30', fg='#a0aec0')
        self.label_status.pack(side='left', pady=5)
        
        # Botão home
        if self.controller:
            btn_home = tk.Button(footer_frame, text="← Menu", 
                               command=lambda: self.controller.show_page("ui_pagina_inicial.py") if self.controller else None,
                               font=('Arial', 8), bg='#2d3748', fg='white',
                               relief='flat', padx=10, pady=3)
            btn_home.pack(side='right', pady=5)
    
    def criar_tabela_tlb(self, parent, height):
        """Cria a tabela TLB compacta"""
        frame_tlb = tk.LabelFrame(parent, text="TLB", font=('Arial', 10, 'bold'), 
                                 bg='#2d3748', fg='white', height=height)
        frame_tlb.pack(fill='x', pady=(0, 5))
        frame_tlb.pack_propagate(False)
        
        # Estilo para treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview", background="#4a5568", foreground="white", 
                       fieldbackground="#4a5568", borderwidth=0, rowheight=20)
        style.configure("Custom.Treeview.Heading", background="#2d3748", foreground="white", font=('Arial', 8))
        
        self.tree_tlb = ttk.Treeview(frame_tlb, columns=('processo', 'vpn', 'pfn'), 
                                    show='headings', height=7, style="Custom.Treeview")
        
        self.tree_tlb.heading('processo', text='Proc')
        self.tree_tlb.heading('vpn', text='VPN')
        self.tree_tlb.heading('pfn', text='PFN')
        
        self.tree_tlb.column('processo', width=80, anchor='center')
        self.tree_tlb.column('vpn', width=80, anchor='center')
        self.tree_tlb.column('pfn', width=80, anchor='center')
        
        self.tree_tlb.pack(fill='both', expand=True, padx=3, pady=3)
    
    def criar_tabela_memoria_principal(self, parent, height):
        """Cria a tabela de Memória Principal compacta"""
        frame_mp = tk.LabelFrame(parent, text="Memória Principal", font=('Arial', 10, 'bold'), 
                                bg='#2d3748', fg='white', height=height)
        frame_mp.pack(fill='x', pady=(0, 5))
        frame_mp.pack_propagate(False)
        
        self.tree_mp = ttk.Treeview(frame_mp, columns=('quadro', 'processo', 'pagina', 'mod'), 
                                   show='headings', height=7, style="Custom.Treeview")
        
        self.tree_mp.heading('quadro', text='Quadro')
        self.tree_mp.heading('processo', text='Proc')
        self.tree_mp.heading('pagina', text='Pág')
        self.tree_mp.heading('mod', text='Mod')
        
        self.tree_mp.column('quadro', width=60, anchor='center')
        self.tree_mp.column('processo', width=60, anchor='center')
        self.tree_mp.column('pagina', width=50, anchor='center')
        self.tree_mp.column('mod', width=40, anchor='center')
        
        self.tree_mp.pack(fill='both', expand=True, padx=3, pady=3)
    
    def criar_tabela_processos(self, parent, height):
        """Cria a tabela de Processos Ativos compacta"""
        frame_proc = tk.LabelFrame(parent, text="Processos", font=('Arial', 10, 'bold'), 
                                  bg='#2d3748', fg='white', height=height)
        frame_proc.pack(fill='both', expand=True)
        frame_proc.pack_propagate(False)
        
        self.tree_proc = ttk.Treeview(frame_proc, columns=('id', 'estado', 'tam', 'pags'), 
                                     show='headings', height=7, style="Custom.Treeview")
        
        self.tree_proc.heading('id', text='ID')
        self.tree_proc.heading('estado', text='Estado')
        self.tree_proc.heading('tam', text='Tam(B)')
        self.tree_proc.heading('pags', text='Págs')
        
        self.tree_proc.column('id', width=40, anchor='center')
        self.tree_proc.column('estado', width=80, anchor='center')
        self.tree_proc.column('tam', width=80, anchor='center')
        self.tree_proc.column('pags', width=50, anchor='center')
        
        self.tree_proc.pack(fill='both', expand=True, padx=3, pady=3)
    
    def criar_tabela_memoria_secundaria(self, parent, height):
        """Cria a tabela de Memória Secundária compacta"""
        frame_ms = tk.LabelFrame(parent, text="Memória Secundária", font=('Arial', 10, 'bold'), 
                                bg='#2d3748', fg='white', height=height)
        frame_ms.pack(fill='both', expand=True)
        frame_ms.pack_propagate(False)
        
        self.tree_ms = ttk.Treeview(frame_ms, columns=('processo', 'pagina'), 
                                   show='headings', height=7, style="Custom.Treeview")
        
        self.tree_ms.heading('processo', text='Processo')
        self.tree_ms.heading('pagina', text='Página')
        
        self.tree_ms.column('processo', width=100, anchor='center')
        self.tree_ms.column('pagina', width=100, anchor='center')
        
        self.tree_ms.pack(fill='both', expand=True, padx=3, pady=3)
    
    def carregar_comandos_arquivo(self):
        """Carrega comandos do arquivo de teste configurado"""
        try:
            with open(ARQ_TESTE, "r", encoding="utf-8") as f: 
                self.comandos = [tuple(line.strip().split()) for line in f if line.strip()]
            return True
        except FileNotFoundError:
            messagebox.showerror("Erro", f"Arquivo de teste '{ARQ_TESTE}' não encontrado.")
            return False
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler o arquivo de teste: {e}")
            return False
    
    def iniciar_simulacao(self):
        """Inicializa a simulação (carrega comandos e prepara o sistema)"""
        if not self.carregar_comandos_arquivo():
            return
            
        try:
            # Inicializar componentes do sistema
            self.mp = MemoriaPrincipal()
            self.tlb = TLB()
            self.processos_lista = []
            self.ciclo_atual = 0
            self.simulacao_iniciada = True
            
            # Atualizar interface
            self.atualizar_interface()
            self.label_status.config(text=f"Pronto - {len(self.comandos)} comandos")
            
            # Habilitar botão próximo
            self.btn_proximo.config(state='normal')
            
            messagebox.showinfo("Simulação Iniciada", 
                              f"Simulação inicializada!\nComandos: {len(self.comandos)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inicializar:\n{str(e)}")
            self.reset_simulacao()
    
    def executar_proximo_ciclo(self):
        """Executa o próximo comando da simulação"""
        if not self.simulacao_iniciada:
            messagebox.showwarning("Aviso", "Inicie a simulação primeiro!")
            return
        
        if self.ciclo_atual >= len(self.comandos):
            messagebox.showinfo("Fim", "Todos os comandos executados!")
            self.label_status.config(text="Simulação finalizada")
            self.btn_proximo.config(state='disabled')
            return
        
        try:
            # Executar comando atual
            comando = self.comandos[self.ciclo_atual]
            self.executar_comando_individual(comando)
            
            # Incrementar ciclo
            self.ciclo_atual += 1
            
            # Atualizar interface
            self.atualizar_interface()
            
            # Atualizar status
            comando_str = ' '.join(comando)
            self.label_status.config(text=f"Executado: {comando_str}")
            
            # Habilitar botão voltar se não estiver no início
            if self.ciclo_atual > 0:
                self.btn_voltar.config(state='normal')
            
            # Verificar se chegou ao fim
            if self.ciclo_atual >= len(self.comandos):
                self.btn_proximo.config(state='disabled')
                self.label_status.config(text="Simulação finalizada")
                messagebox.showinfo("Concluído", "Simulação finalizada!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar:\n{str(e)}")
    
    def executar_comando_individual(self, comando):
        """Executa um comando individual utilizando a lógica do main.py"""
        if not comando:
            return
            
        id_processo = int(comando[0][1:])  # Remove 'P' e converte para int
        tipo_comando = comando[1].upper()
        
        # Encontrar processo existente
        processo_atual = next((p for p in self.processos_lista if p.id == id_processo), None)
        
        if not processo_atual and tipo_comando != "C":
            print(f"Erro: Tentando operar no processo P{id_processo} que não existe.")
            return
        
        if tipo_comando == "C":  # Criar processo
            tamanho = int(comando[2])
            unidade = comando[3].upper()
            tam_processo_bytes = tamanho * MAPA_UNIDADES[unidade]
            
            novo_processo = Processo(id_processo, tam_processo_bytes)
            self.processos_lista.append(novo_processo)
            novo_processo.estado = "Pronto"
            
        elif processo_atual and self.mp and self.tlb: # Garante que a simulação foi iniciada
            if tipo_comando in ["R", "P", "W"]:
                match = re.search(r'\((\d+)\)', comando[2])
                addr = int(match.group(1)) if match else int(comando[2])
                tratar_acesso_memoria(processo_atual, addr, self.tlb, self.mp, tipo_comando, self.processos_lista)
            
            elif tipo_comando == "I":
                processo_atual.estado = "Bloqueado"
            
            elif tipo_comando == "T":
                processo_atual.estado = "Finalizado"
                if self.tlb:
                    self.tlb.invalidar_processo(id_processo)
                self.processos_lista = [p for p in self.processos_lista if p.id != id_processo]
    
    def voltar_ciclo(self):
        """Volta para o ciclo anterior (reinicia a simulação até o ciclo anterior)"""
        if self.ciclo_atual <= 0:
            return
        
        # Confirmar ação
        resposta = messagebox.askyesno("Confirmar", 
                                     "Voltar um ciclo irá reiniciar a simulação. Continuar?")
        if not resposta:
            return
        
        try:
            # Salvar ciclo alvo
            ciclo_alvo = self.ciclo_atual - 1
            
            # Reinicializar sistema
            self.mp = MemoriaPrincipal()
            self.tlb = TLB()
            self.processos_lista = []
            
            # Re-executar comandos até o ciclo alvo
            for i in range(ciclo_alvo):
                comando = self.comandos[i]
                self.executar_comando_individual(comando)
            
            # Atualizar ciclo atual
            self.ciclo_atual = ciclo_alvo
            
            # Atualizar interface
            self.atualizar_interface()
            
            # Reabilitar botão próximo se necessário
            if self.ciclo_atual < len(self.comandos):
                self.btn_proximo.config(state='normal')
            
            # Desabilitar botão voltar se estiver no início
            if self.ciclo_atual <= 0:
                self.btn_voltar.config(state='disabled')
            
            self.label_status.config(text=f"Voltou para ciclo {self.ciclo_atual}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao voltar:\n{str(e)}")
            self.reset_simulacao()
    
    def atualizar_interface(self):
        """Atualiza a interface com o estado atual do sistema"""
        # Atualizar labels de informação
        self.label_ciclo.config(text=f"Ciclo: {self.ciclo_atual}")
        
        # Atualizar tabela TLB
        self.tree_tlb.delete(*self.tree_tlb.get_children())
        if self.tlb:
            for entrada in self.tlb.entradas:
                self.tree_tlb.insert('', 'end', values=(f"P{entrada.id_processo}", entrada.num_pagina_virtual, entrada.num_quadro))
        
        # Atualizar tabela de Memória Principal
        self.tree_mp.delete(*self.tree_mp.get_children())
        if self.mp:
            for quadro in self.mp.quadros:
                if quadro.ocupado and quadro.pagina:
                    mod_str = "S" if quadro.pagina.modificada else "N"
                    self.tree_mp.insert('', 'end', values=(
                        quadro.id_quadro, f"P{quadro.pagina.id_processo}", 
                        quadro.pagina.id_pagina, mod_str
                    ))
        
        # Atualizar tabela de Processos
        self.tree_proc.delete(*self.tree_proc.get_children())
        for processo in self.processos_lista:
            self.tree_proc.insert('', 'end', values=(
                f"P{processo.id}", processo.estado, processo.tamanho_bytes, processo.quantidade_paginas
            ))
        
        # Atualizar tabela de Memória Secundária
        self.tree_ms.delete(*self.tree_ms.get_children())
        for processo in self.processos_lista:
            # Iterar sobre a tabela de páginas para encontrar as que não estão presentes
            for i, entrada_tp in enumerate(processo.tabela_paginas.entradas):
                if not entrada_tp.bit_presenca:
                    self.tree_ms.insert('', 'end', values=(f"P{processo.id}", i))
        
        # Atualizar estatísticas da TLB
        if self.tlb:
            total_acessos = self.tlb.hits + self.tlb.misses
            taxa_acerto = (self.tlb.hits / total_acessos * 100) if total_acessos > 0 else 0
            self.label_acertos.config(text=f"Acertos: {self.tlb.hits}")
            self.label_falhas.config(text=f"Falhas: {self.tlb.misses}")
            self.label_taxa.config(text=f"Taxa: {taxa_acerto:.1f}%")
    
    def reset_simulacao(self):
        """Reseta completamente a simulação"""
        # Resetar variáveis do sistema
        self.mp = None
        self.tlb = None
        self.processos_lista = []
        self.comandos = []
        self.ciclo_atual = 0
        self.simulacao_iniciada = False
        
        # Limpar todas as tabelas
        self.tree_tlb.delete(*self.tree_tlb.get_children())
        self.tree_mp.delete(*self.tree_mp.get_children())
        self.tree_proc.delete(*self.tree_proc.get_children())
        self.tree_ms.delete(*self.tree_ms.get_children())
        
        # Resetar labels informativos
        self.label_ciclo.config(text="Ciclo: 0")
        self.label_acertos.config(text="Acertos: 0")
        self.label_falhas.config(text="Falhas: 0")
        self.label_taxa.config(text="Taxa: 0%")
        self.label_status.config(text="Aguardando início")
        
        # Desabilitar botões de navegação
        self.btn_voltar.config(state='disabled')
        self.btn_proximo.config(state='disabled')
        
        messagebox.showinfo("Reset", "Simulação resetada!")