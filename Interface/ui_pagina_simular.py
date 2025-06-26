import tkinter as tk
from tkinter import ttk, messagebox
import re
import sys 
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from memoriaPrincipal import MemoriaPrincipal
from config import *
from tlb import TLB
from classesProcessos import Processo
from main import tratar_acesso_memoria


class Tela_Simular(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#181f30')
        
        # Configurar tamanho da janela para grande
        if hasattr(parent, 'geometry'):
            parent.geometry('1200x800')  # Tamanho grande
            parent.minsize(1200, 800)    # Tamanho mínimo
        
        # Variáveis da simulação
        self.mp = None
        self.tlb = None
        self.processos_lista = []
        self.comandos = []
        self.ciclo_atual = 0
        self.simulacao_iniciada = False
        
        # Criar interface
        self.criar_interface()
        
    def criar_interface(self):
        """Cria todos os elementos da interface"""
        # Frame principal
        main_frame = tk.Frame(self, bg='#181f30')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Título
        titulo = tk.Label(main_frame, text="Simulador de Gerenciamento de Memória", 
                         font=('Arial', 20, 'bold'), bg='#181f30', fg='white')
        titulo.pack(pady=(0, 15))
        
        # Frame superior (controles e informações)
        top_frame = tk.Frame(main_frame, bg='#181f30')
        top_frame.pack(fill='x', pady=(0, 15))
        
        # Botões de controle
        controles_frame = tk.Frame(top_frame, bg='#181f30')
        controles_frame.pack(side='left')
        
        btn_iniciar = tk.Button(controles_frame, text="Iniciar Simulação", 
                               command=self.iniciar_simulacao,
                               font=('Arial', 14, 'bold'), bg='#38a169', fg='white',
                               relief='flat', padx=25, pady=12)
        btn_iniciar.pack(side='left', padx=(0, 15))
        
        btn_reset = tk.Button(controles_frame, text="Reset", 
                            command=self.reset_simulacao,
                            font=('Arial', 14, 'bold'), bg='#e53e3e', fg='white',
                            relief='flat', padx=25, pady=12)
        btn_reset.pack(side='left')
        
        # Informações do ciclo atual
        info_frame = tk.Frame(top_frame, bg='#181f30')
        info_frame.pack(side='right')
        
        self.label_arquivo = tk.Label(info_frame, text=f"Arquivo: {ARQ_TESTE}", 
                                    font=('Arial', 12), bg='#181f30', fg='#a0aec0')
        self.label_arquivo.pack(anchor='e')
        
        self.label_ciclo = tk.Label(info_frame, text=f"Ciclo: {self.ciclo_atual}", 
                                   font=('Arial', 16, 'bold'), bg='#181f30', fg='white')
        self.label_ciclo.pack(anchor='e')
        
        self.label_comando = tk.Label(info_frame, text="Comando atual: -", 
                                    font=('Arial', 12), bg='#181f30', fg='#a0aec0')
        self.label_comando.pack(anchor='e')
        
        # Frame central (tabelas) - Layout horizontal melhorado
        central_frame = tk.Frame(main_frame, bg='#181f30')
        central_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Frame esquerdo (TLB e Estatísticas) - Largura fixa
        left_frame = tk.Frame(central_frame, bg='#181f30', width=450)
        left_frame.pack(side='left', fill='y', padx=(0, 10))
        left_frame.pack_propagate(False)
        
        # TLB
        self.criar_tabela_tlb(left_frame)
        
        # Estatísticas
        self.criar_frame_estatisticas(left_frame)
        
        # Frame direito (Memórias) - Expande para ocupar o resto
        right_frame = tk.Frame(central_frame, bg='#181f30')
        right_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Memória Principal
        self.criar_tabela_memoria_principal(right_frame)
        
        # Processos Ativos
        self.criar_tabela_processos(right_frame)
        
        # Frame inferior (botões de navegação e configurações)
        bottom_frame = tk.Frame(main_frame, bg='#181f30')
        bottom_frame.pack(fill='x', pady=(15, 0))
        
        # Botões de navegação - DESTACADOS e MAIORES
        nav_frame = tk.Frame(bottom_frame, bg='#2d3748', relief='raised', bd=3)
        nav_frame.pack(pady=(0, 20), padx=80, fill='x')
        
        nav_title = tk.Label(nav_frame, text="Controle de Execução", 
                            font=('Arial', 16, 'bold'), bg='#2d3748', fg='white')
        nav_title.pack(pady=(15, 10))
        
        buttons_frame = tk.Frame(nav_frame, bg='#2d3748')
        buttons_frame.pack(pady=(0, 15))
        
        self.btn_voltar = tk.Button(buttons_frame, text="◀ Voltar", 
                                   command=self.voltar_ciclo,
                                   font=('Arial', 14, 'bold'), bg='#4299e1', fg='white',
                                   width=15, height=3, relief='flat', state='disabled')
        self.btn_voltar.pack(side='left', padx=(0, 30))
        
        self.label_ciclo_nav = tk.Label(buttons_frame, text=f"Ciclo {self.ciclo_atual}", 
                                       font=('Arial', 20, 'bold'), bg='#2d3748', fg='white')
        self.label_ciclo_nav.pack(side='left', padx=40)
        
        self.btn_proximo = tk.Button(buttons_frame, text="Próximo ▶", 
                                    command=self.executar_proximo_ciclo,
                                    font=('Arial', 14, 'bold'), bg='#38a169', fg='white',
                                    width=15, height=3, relief='flat', state='disabled')
        self.btn_proximo.pack(side='left', padx=(30, 0))
        
        # Status da simulação
        self.label_status = tk.Label(nav_frame, text="Status: Aguardando início", 
                                    font=('Arial', 12), bg='#2d3748', fg='#a0aec0')
        self.label_status.pack(pady=(0, 15))
        
        # Informações de configuração
        config_frame = tk.Frame(bottom_frame, bg='#181f30')
        config_frame.pack(pady=(0, 15))
        
        config_info = tk.Label(config_frame, 
                              text=f"Configurações: Mem. Principal: {TAMANHO_MEMORIA_P}KB | "
                                   f"Página/Quadro: {TAMANHO_PAGINA_QUADRO}B | "
                                   f"TLB: {NUMERO_LINHAS_TLB} linhas | "
                                   f"Política: {'LRU' if POLITICA_SUB == 0 else 'Relógio'}",
                              font=('Arial', 11), bg='#181f30', fg='#a0aec0')
        config_info.pack()
        
        # Botão voltar para página inicial
        if self.controller:
            btn_home = tk.Button(bottom_frame, text="← Voltar ao Menu", 
                               command=lambda: self.controller.show_page("ui_pagina_inicial.py"),
                               font=('Arial', 12), bg='#2d3748', fg='white',
                               relief='flat', padx=20, pady=8)
            btn_home.pack(anchor='w', pady=(15, 0))
    
    def criar_tabela_tlb(self, parent):
        """Cria a tabela TLB"""
        frame_tlb = tk.LabelFrame(parent, text="TLB (Translation Lookaside Buffer)", 
                                 font=('Arial', 13, 'bold'), bg='#2d3748', fg='white')
        frame_tlb.pack(fill='both', expand=True, pady=(0, 15))
        
        # Estilo para treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview", 
                       background="#4a5568", 
                       foreground="white", 
                       fieldbackground="#4a5568", 
                       borderwidth=0,
                       rowheight=25)  # Altura das linhas
        style.configure("Custom.Treeview.Heading", 
                       background="#2d3748", 
                       foreground="white",
                       font=('Arial', 11, 'bold'))
        
        self.tree_tlb = ttk.Treeview(frame_tlb, columns=('processo', 'vpn', 'pfn'), 
                                    show='headings', height=10, style="Custom.Treeview")
        
        self.tree_tlb.heading('processo', text='Processo')
        self.tree_tlb.heading('vpn', text='VPN')
        self.tree_tlb.heading('pfn', text='PFN')
        
        self.tree_tlb.column('processo', width=120, anchor='center')
        self.tree_tlb.column('vpn', width=120, anchor='center')
        self.tree_tlb.column('pfn', width=120, anchor='center')
        
        # Scrollbar para TLB
        scrollbar_tlb = ttk.Scrollbar(frame_tlb, orient="vertical", command=self.tree_tlb.yview)
        self.tree_tlb.configure(yscrollcommand=scrollbar_tlb.set)
        
        self.tree_tlb.pack(side="left", fill='both', expand=True, padx=8, pady=8)
        scrollbar_tlb.pack(side="right", fill="y", padx=(0, 8), pady=8)
    
    def criar_frame_estatisticas(self, parent):
        """Cria o frame de estatísticas"""
        frame_stats = tk.LabelFrame(parent, text="Estatísticas da TLB", 
                                   font=('Arial', 13, 'bold'), bg='#2d3748', fg='white')
        frame_stats.pack(fill='x', pady=(0, 15))
        
        stats_content = tk.Frame(frame_stats, bg='#2d3748')
        stats_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        self.label_acertos = tk.Label(stats_content, text="Acertos: 0", 
                                     font=('Arial', 13, 'bold'), bg='#2d3748', fg='#68d391')
        self.label_acertos.pack(anchor='w', pady=3)
        
        self.label_falhas = tk.Label(stats_content, text="Falhas: 0", 
                                    font=('Arial', 13, 'bold'), bg='#2d3748', fg='#f56565')
        self.label_falhas.pack(anchor='w', pady=3)
        
        self.label_taxa = tk.Label(stats_content, text="Taxa de Acerto: 0%", 
                                  font=('Arial', 13, 'bold'), bg='#2d3748', fg='#63b3ed')
        self.label_taxa.pack(anchor='w', pady=3)
    
    def criar_tabela_memoria_principal(self, parent):
        """Cria a tabela de Memória Principal"""
        frame_mp = tk.LabelFrame(parent, text="Memória Principal", 
                                font=('Arial', 13, 'bold'), bg='#2d3748', fg='white')
        frame_mp.pack(fill='both', expand=True, pady=(0, 15))
        
        self.tree_mp = ttk.Treeview(frame_mp, columns=('quadro', 'processo', 'pagina', 'modificada'), 
                                   show='headings', height=12, style="Custom.Treeview")
        
        self.tree_mp.heading('quadro', text='Quadro')
        self.tree_mp.heading('processo', text='Processo')
        self.tree_mp.heading('pagina', text='Página')
        self.tree_mp.heading('modificada', text='Modificada')
        
        self.tree_mp.column('quadro', width=100, anchor='center')
        self.tree_mp.column('processo', width=120, anchor='center')
        self.tree_mp.column('pagina', width=100, anchor='center')
        self.tree_mp.column('modificada', width=120, anchor='center')
        
        # Scrollbar para Memória Principal
        scrollbar_mp = ttk.Scrollbar(frame_mp, orient="vertical", command=self.tree_mp.yview)
        self.tree_mp.configure(yscrollcommand=scrollbar_mp.set)
        
        self.tree_mp.pack(side="left", fill='both', expand=True, padx=8, pady=8)
        scrollbar_mp.pack(side="right", fill="y", padx=(0, 8), pady=8)
    
    def criar_tabela_processos(self, parent):
        """Cria a tabela de Processos Ativos"""
        frame_proc = tk.LabelFrame(parent, text="Processos Ativos", 
                                  font=('Arial', 13, 'bold'), bg='#2d3748', fg='white')
        frame_proc.pack(fill='both', expand=True)
        
        self.tree_proc = ttk.Treeview(frame_proc, columns=('id', 'estado', 'tamanho', 'paginas'), 
                                     show='headings', height=8, style="Custom.Treeview")
        
        self.tree_proc.heading('id', text='ID')
        self.tree_proc.heading('estado', text='Estado')
        self.tree_proc.heading('tamanho', text='Tamanho (B)')
        self.tree_proc.heading('paginas', text='Páginas')
        
        self.tree_proc.column('id', width=80, anchor='center')
        self.tree_proc.column('estado', width=100, anchor='center')
        self.tree_proc.column('tamanho', width=120, anchor='center')
        self.tree_proc.column('paginas', width=100, anchor='center')
        
        # Scrollbar para Processos
        scrollbar_proc = ttk.Scrollbar(frame_proc, orient="vertical", command=self.tree_proc.yview)
        self.tree_proc.configure(yscrollcommand=scrollbar_proc.set)
        
        self.tree_proc.pack(side="left", fill='both', expand=True, padx=8, pady=8)
        scrollbar_proc.pack(side="right", fill="y", padx=(0, 8), pady=8)
    
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
            self.label_status.config(text=f"Status: Pronto - {len(self.comandos)} comandos carregados")
            
            # Habilitar botão próximo
            self.btn_proximo.config(state='normal')
            
            messagebox.showinfo("Simulação Iniciada", 
                              f"Simulação inicializada com sucesso!\n"
                              f"Total de comandos: {len(self.comandos)}\n"
                              f"Use o botão 'Próximo' para executar os comandos.")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inicializar simulação:\n{str(e)}")
            self.reset_simulacao()
    
    def executar_proximo_ciclo(self):
        """Executa o próximo comando da simulação"""
        if not self.simulacao_iniciada:
            messagebox.showwarning("Aviso", "Inicie a simulação primeiro!")
            return
        
        if self.ciclo_atual >= len(self.comandos):
            messagebox.showinfo("Fim", "Todos os comandos foram executados!")
            self.label_status.config(text="Status: Simulação finalizada")
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
            self.label_status.config(text=f"Status: Executado - {comando_str}")
            
            # Habilitar botão voltar se não estiver no início
            if self.ciclo_atual > 0:
                self.btn_voltar.config(state='normal')
            
            # Verificar se chegou ao fim
            if self.ciclo_atual >= len(self.comandos):
                self.btn_proximo.config(state='disabled')
                self.label_status.config(text="Status: Simulação finalizada")
                messagebox.showinfo("Concluído", "Simulação finalizada com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar comando:\n{str(e)}")
    
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
            tamanho, unidade = int(comando[2]), comando[3]
            if unidade == "KB": 
                tam_processo = tamanho * 1024
            elif unidade == "MB": 
                tam_processo = tamanho * 1024 * 1024
            else: 
                tam_processo = tamanho * 1024 * 1024 * 1024
            
            novo_processo = Processo(id_processo, tam_processo)
            self.processos_lista.append(novo_processo)
            novo_processo.estado = "P"
            
        elif tipo_comando in ["R", "P", "W"]:  # Acesso à memória
            # Extrair endereço virtual
            match = re.search(r'\((\d+)\)', comando[2])
            if match:
                endereco_virtual = int(match.group(1))
            else:
                try:
                    endereco_virtual = int(comando[2])
                except ValueError:
                    print(f"Erro: Formato de endereço inválido no comando: {' '.join(comando)}")
                    return
            
            # Usar a função tratar_acesso_memoria do main.py
            tratar_acesso_memoria(processo_atual, endereco_virtual, self.tlb, 
                                self.mp, tipo_comando, self.processos_lista)
            
        elif tipo_comando == "I":  # I/O
            processo_atual.estado = "B"
            
        elif tipo_comando == "T":  # Terminar processo
            processo_atual.estado = "F"
            self.tlb.invalidar_processo(id_processo)
            self.processos_lista.remove(processo_atual)
    
    def voltar_ciclo(self):
        """Volta para o ciclo anterior (reinicia a simulação até o ciclo anterior)"""
        if self.ciclo_atual <= 0:
            return
        
        # Confirmar ação
        resposta = messagebox.askyesno("Confirmar", 
                                     "Voltar um ciclo irá reiniciar a simulação até o ciclo anterior. Continuar?")
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
            
            self.label_status.config(text=f"Status: Voltou para ciclo {self.ciclo_atual}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao voltar ciclo:\n{str(e)}")
            self.reset_simulacao()
    
    def atualizar_interface(self):
        """Atualiza a interface com o estado atual do sistema"""
        # Atualizar labels de informação
        self.label_ciclo.config(text=f"Ciclo: {self.ciclo_atual}")
        self.label_ciclo_nav.config(text=f"Ciclo {self.ciclo_atual}")
        
        # Mostrar próximo comando se existir
        if self.ciclo_atual < len(self.comandos):
            proximo_comando = ' '.join(self.comandos[self.ciclo_atual])
            self.label_comando.config(text=f"Próximo: {proximo_comando}")
        else:
            self.label_comando.config(text="Comando: Simulação finalizada")
        
        # Atualizar tabela TLB
        self.tree_tlb.delete(*self.tree_tlb.get_children())
        if self.tlb:
            for (id_proc, vpn), entrada in self.tlb.entradas.items():
                self.tree_tlb.insert('', 'end', values=(f"P{id_proc}", vpn, entrada.numeroFrameFisico))
        
        # Atualizar tabela de Memória Principal
        self.tree_mp.delete(*self.tree_mp.get_children())
        if self.mp:
            for quadro in self.mp.quadros:
                if quadro.pagina:
                    mod_str = "Sim" if quadro.pagina.modificada else "Não"
                    self.tree_mp.insert('', 'end', values=(
                        quadro.idQuadro, f"P{quadro.pagina.idProcesso}", 
                        quadro.pagina.idPagina, mod_str
                    ))
        
        # Atualizar tabela de Processos
        self.tree_proc.delete(*self.tree_proc.get_children())
        for processo in self.processos_lista:
            self.tree_proc.insert('', 'end', values=(
                f"P{processo.id}", processo.estado, processo.tamanho, processo.quantidadePaginas
            ))
        
        # Atualizar estatísticas da TLB
        if self.tlb:
            stats = self.tlb.obterEstatisticas()
            self.label_acertos.config(text=f"Acertos: {stats.get('acertos', 0)}")
            self.label_falhas.config(text=f"Falhas: {stats.get('falhas', 0)}")
            self.label_taxa.config(text=f"Taxa de Acerto: {stats.get('taxaAcertos', 0):.1f}%")
    
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
        
        # Resetar labels informativos
        self.label_ciclo.config(text="Ciclo: 0")
        self.label_ciclo_nav.config(text="Ciclo 0")
        self.label_comando.config(text="Comando: -")
        self.label_acertos.config(text="Acertos: 0")
        self.label_falhas.config(text="Falhas: 0")
        self.label_taxa.config(text="Taxa de Acerto: 0%")
        self.label_status.config(text="Status: Aguardando início")
        
        # Desabilitar botões de navegação
        self.btn_voltar.config(state='disabled')
        self.btn_proximo.config(state='disabled')
        
        messagebox.showinfo("Reset", "Simulação resetada com sucesso!")