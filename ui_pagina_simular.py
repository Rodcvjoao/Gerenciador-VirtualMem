import tkinter as tk
from tkinter import ttk, messagebox
import re
from memoriaPrincipal import MemoriaPrincipal
from tlb import TLB
from classesProcessos import Processo
from config import *
from main import tratar_acesso_memoria

class Tela_Simular(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='#181f30')
        
        # Variáveis da simulação
        self.mp = None
        self.tlb = None
        self.processos_lista = []
        self.comandos = []
        self.ciclo_atual = 0
        self.historico_completo = []
        self.simulacao_executada = False
        
        # Criar interface
        self.criar_interface()
        
    def criar_interface(self):
        """Cria todos os elementos da interface"""
        # Frame principal
        main_frame = tk.Frame(self, bg='#181f30')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        titulo = tk.Label(main_frame, text="Simulador de Gerenciamento de Memória", 
                         font=('Arial', 16, 'bold'), bg='#181f30', fg='white')
        titulo.pack(pady=(0, 10))
        
        # Frame superior (controles e informações)
        top_frame = tk.Frame(main_frame, bg='#181f30')
        top_frame.pack(fill='x', pady=(0, 10))
        
        # Botões de controle
        controles_frame = tk.Frame(top_frame, bg='#181f30')
        controles_frame.pack(side='left')
        
        btn_executar = tk.Button(controles_frame, text="Executar Simulação", 
                               command=self.executar_simulacao_completa,
                               font=('Arial', 12), bg='#38a169', fg='white',
                               relief='flat', padx=20, pady=8)
        btn_executar.pack(side='left', padx=(0, 10))
        
        btn_reset = tk.Button(controles_frame, text="Reset", 
                            command=self.reset_simulacao,
                            font=('Arial', 12), bg='#e53e3e', fg='white',
                            relief='flat', padx=20, pady=8)
        btn_reset.pack(side='left')
        
        # Informações do ciclo atual
        info_frame = tk.Frame(top_frame, bg='#181f30')
        info_frame.pack(side='right')
        
        self.label_arquivo = tk.Label(info_frame, text=f"Arquivo: {ARQ_TESTE}", 
                                    font=('Arial', 10), bg='#181f30', fg='#a0aec0')
        self.label_arquivo.pack(anchor='e')
        
        self.label_ciclo = tk.Label(info_frame, text=f"Ciclo: {self.ciclo_atual}", 
                                   font=('Arial', 12, 'bold'), bg='#181f30', fg='white')
        self.label_ciclo.pack(anchor='e')
        
        self.label_comando = tk.Label(info_frame, text="Comando atual: -", 
                                    font=('Arial', 10), bg='#181f30', fg='#a0aec0')
        self.label_comando.pack(anchor='e')
        
        # Frame central (tabelas)
        central_frame = tk.Frame(main_frame, bg='#181f30')
        central_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Frame esquerdo (TLB e Estatísticas)
        left_frame = tk.Frame(central_frame, bg='#181f30')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # TLB
        self.criar_tabela_tlb(left_frame)
        
        # Estatísticas
        self.criar_frame_estatisticas(left_frame)
        
        # Frame direito (Memórias)
        right_frame = tk.Frame(central_frame, bg='#181f30')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Memória Principal
        self.criar_tabela_memoria_principal(right_frame)
        
        # Processos Ativos
        self.criar_tabela_processos(right_frame)
        
        # Frame inferior (botões de navegação e configurações)
        bottom_frame = tk.Frame(main_frame, bg='#181f30')
        bottom_frame.pack(fill='x', pady=(10, 0))
        
        # Informações de configuração
        config_frame = tk.Frame(bottom_frame, bg='#181f30')
        config_frame.pack(pady=(0, 10))
        
        config_info = tk.Label(config_frame, 
                              text=f"Configurações: Mem. Principal: {TAMANHO_MEMORIA_P}KB | "
                                   f"Página/Quadro: {TAMANHO_PAGINA_QUADRO}B | "
                                   f"TLB: {NUMERO_LINHAS_TLB} linhas | "
                                   f"Política: {'LRU' if POLITICA_SUB == 0 else 'Relógio'}",
                              font=('Arial', 9), bg='#181f30', fg='#a0aec0')
        config_info.pack()
        
        # Botões de navegação
        nav_frame = tk.Frame(bottom_frame, bg='#181f30')
        nav_frame.pack()
        
        self.btn_voltar = tk.Button(nav_frame, text="◀ Voltar", 
                                   command=self.voltar_ciclo,
                                   font=('Arial', 12), bg='#4a5568', fg='white',
                                   width=10, height=2, relief='flat', state='disabled')
        self.btn_voltar.pack(side='left', padx=(0, 20))
        
        self.label_ciclo_nav = tk.Label(nav_frame, text=f"Ciclo {self.ciclo_atual}", 
                                       font=('Arial', 14, 'bold'), bg='#181f30', fg='white')
        self.label_ciclo_nav.pack(side='left', padx=20)
        
        self.btn_avancar = tk.Button(nav_frame, text="Avançar ▶", 
                                    command=self.avancar_ciclo,
                                    font=('Arial', 12), bg='#4a5568', fg='white',
                                    width=10, height=2, relief='flat', state='disabled')
        self.btn_avancar.pack(side='left', padx=(20, 0))
        
        # Botão voltar para página inicial
        if self.controller:
            btn_home = tk.Button(bottom_frame, text="← Voltar ao Menu", 
                               command=lambda: self.controller.show_page("ui_pagina_inicial.py"),
                               font=('Arial', 10), bg='#2d3748', fg='white',
                               relief='flat', padx=15, pady=5)
            btn_home.pack(anchor='w', pady=(10, 0))
    
    def criar_tabela_tlb(self, parent):
        """Cria a tabela TLB"""
        frame_tlb = tk.LabelFrame(parent, text="TLB (Translation Lookaside Buffer)", 
                                 font=('Arial', 11, 'bold'), bg='#2d3748', fg='white')
        frame_tlb.pack(fill='both', expand=True, pady=(0, 10))
        
        # Estilo para treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Treeview", background="#4a5568", foreground="white", 
                       fieldbackground="#4a5568", borderwidth=0)
        style.configure("Custom.Treeview.Heading", background="#2d3748", foreground="white")
        
        self.tree_tlb = ttk.Treeview(frame_tlb, columns=('processo', 'vpn', 'pfn'), 
                                    show='headings', height=6, style="Custom.Treeview")
        
        self.tree_tlb.heading('processo', text='Processo')
        self.tree_tlb.heading('vpn', text='VPN')
        self.tree_tlb.heading('pfn', text='PFN')
        
        self.tree_tlb.column('processo', width=80, anchor='center')
        self.tree_tlb.column('vpn', width=80, anchor='center')
        self.tree_tlb.column('pfn', width=80, anchor='center')
        
        self.tree_tlb.pack(fill='both', expand=True, padx=5, pady=5)
    
    def criar_frame_estatisticas(self, parent):
        """Cria o frame de estatísticas"""
        frame_stats = tk.LabelFrame(parent, text="Estatísticas da TLB", 
                                   font=('Arial', 11, 'bold'), bg='#2d3748', fg='white')
        frame_stats.pack(fill='x', pady=(0, 10))
        
        stats_content = tk.Frame(frame_stats, bg='#2d3748')
        stats_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.label_acertos = tk.Label(stats_content, text="Acertos: 0", 
                                     font=('Arial', 11), bg='#2d3748', fg='#68d391')
        self.label_acertos.pack(anchor='w', pady=2)
        
        self.label_falhas = tk.Label(stats_content, text="Falhas: 0", 
                                    font=('Arial', 11), bg='#2d3748', fg='#f56565')
        self.label_falhas.pack(anchor='w', pady=2)
        
        self.label_taxa = tk.Label(stats_content, text="Taxa de Acerto: 0%", 
                                  font=('Arial', 11), bg='#2d3748', fg='#63b3ed')
        self.label_taxa.pack(anchor='w', pady=2)
    
    def criar_tabela_memoria_principal(self, parent):
        """Cria a tabela de Memória Principal"""
        frame_mp = tk.LabelFrame(parent, text="Memória Principal", 
                                font=('Arial', 11, 'bold'), bg='#2d3748', fg='white')
        frame_mp.pack(fill='both', expand=True, pady=(0, 10))
        
        self.tree_mp = ttk.Treeview(frame_mp, columns=('quadro', 'processo', 'pagina', 'modificada'), 
                                   show='headings', height=8, style="Custom.Treeview")
        
        self.tree_mp.heading('quadro', text='Quadro')
        self.tree_mp.heading('processo', text='Processo')
        self.tree_mp.heading('pagina', text='Página')
        self.tree_mp.heading('modificada', text='Mod.')
        
        self.tree_mp.column('quadro', width=60, anchor='center')
        self.tree_mp.column('processo', width=70, anchor='center')
        self.tree_mp.column('pagina', width=60, anchor='center')
        self.tree_mp.column('modificada', width=50, anchor='center')
        
        self.tree_mp.pack(fill='both', expand=True, padx=5, pady=5)
    
    def criar_tabela_processos(self, parent):
        """Cria a tabela de Processos Ativos"""
        frame_proc = tk.LabelFrame(parent, text="Processos Ativos", 
                                  font=('Arial', 11, 'bold'), bg='#2d3748', fg='white')
        frame_proc.pack(fill='both', expand=True)
        
        self.tree_proc = ttk.Treeview(frame_proc, columns=('id', 'estado', 'tamanho', 'paginas'), 
                                     show='headings', height=6, style="Custom.Treeview")
        
        self.tree_proc.heading('id', text='ID')
        self.tree_proc.heading('estado', text='Estado')
        self.tree_proc.heading('tamanho', text='Tamanho (B)')
        self.tree_proc.heading('paginas', text='Páginas')
        
        self.tree_proc.column('id', width=40, anchor='center')
        self.tree_proc.column('estado', width=60, anchor='center')
        self.tree_proc.column('tamanho', width=80, anchor='center')
        self.tree_proc.column('paginas', width=60, anchor='center')
        
        self.tree_proc.pack(fill='both', expand=True, padx=5, pady=5)
    
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
    
    def executar_simulacao_completa(self):
        """Executa a simulação completa utilizando as funções do main.py"""
        if not self.carregar_comandos_arquivo():
            return
            
        try:
            # Inicializar componentes do sistema
            self.mp = MemoriaPrincipal()
            self.tlb = TLB()
            self.processos_lista = []
            self.historico_completo = []
            
            # Capturar estado inicial
            estado_inicial = self.capturar_estado_sistema(0, "Inicial")
            self.historico_completo.append(estado_inicial)
            
            # Executar cada comando da simulação
            for ciclo, comando in enumerate(self.comandos, 1):
                self.executar_comando_individual(comando)
                
                # Capturar estado após cada comando
                estado = self.capturar_estado_sistema(ciclo, ' '.join(comando))
                self.historico_completo.append(estado)
            
            # Configurar interface para navegação
            self.ciclo_atual = 0
            self.simulacao_executada = True
            self.atualizar_interface()
            
            # Habilitar botões de navegação
            self.btn_avancar.config(state='normal')
            
            messagebox.showinfo("Sucesso", 
                              f"Simulação executada com sucesso!\n"
                              f"Total de comandos: {len(self.comandos)}\n"
                              f"Estados salvos: {len(self.historico_completo)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante a simulação:\n{str(e)}")
            self.reset_simulacao()
    
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
    
    def capturar_estado_sistema(self, ciclo, comando):
        """Captura o estado atual do sistema"""
        estado = {
            'ciclo': ciclo,
            'comando': comando,
            'tlb_entradas': [],
            'memoria_principal': [],
            'processos': [],
            'estatisticas': {}
        }
        
        # Capturar estado da TLB
        if self.tlb:
            for (id_proc, vpn), entrada in self.tlb.entradas.items():
                estado['tlb_entradas'].append((id_proc, vpn, entrada.numeroFrameFisico))
            
            stats = self.tlb.obterEstatisticas()
            estado['estatisticas'] = stats
        
        # Capturar estado da Memória Principal
        if self.mp:
            for quadro in self.mp.quadros:
                if quadro.pagina:
                    estado['memoria_principal'].append({
                        'quadro': quadro.idQuadro,
                        'processo': quadro.pagina.idProcesso,
                        'pagina': quadro.pagina.idPagina,
                        'modificada': quadro.pagina.modificada
                    })
        
        # Capturar estado dos Processos
        for processo in self.processos_lista:
            estado['processos'].append({
                'id': processo.id,
                'estado': processo.estado,
                'tamanho': processo.tamanho,
                'paginas': processo.quantidadePaginas
            })
        
        return estado
    
    def voltar_ciclo(self):
        """Volta para o ciclo anterior"""
        if self.ciclo_atual > 0:
            self.ciclo_atual -= 1
            self.atualizar_interface()
    
    def avancar_ciclo(self):
        """Avança para o próximo ciclo"""
        if self.ciclo_atual < len(self.historico_completo) - 1:
            self.ciclo_atual += 1
            self.atualizar_interface()
    
    def atualizar_interface(self):
        """Atualiza a interface com o estado do ciclo atual"""
        if not self.historico_completo or self.ciclo_atual >= len(self.historico_completo):
            return
        
        estado = self.historico_completo[self.ciclo_atual]
        
        # Atualizar labels de informação
        self.label_ciclo.config(text=f"Ciclo: {estado['ciclo']}")
        self.label_ciclo_nav.config(text=f"Ciclo {estado['ciclo']}")
        self.label_comando.config(text=f"Comando: {estado['comando']}")
        
        # Atualizar tabela TLB
        self.tree_tlb.delete(*self.tree_tlb.get_children())
        for processo, vpn, pfn in estado['tlb_entradas']:
            self.tree_tlb.insert('', 'end', values=(f"P{processo}", vpn, pfn))
        
        # Atualizar tabela de Memória Principal
        self.tree_mp.delete(*self.tree_mp.get_children())
        for entry in estado['memoria_principal']:
            mod_str = "Sim" if entry['modificada'] else "Não"
            self.tree_mp.insert('', 'end', values=(
                entry['quadro'], f"P{entry['processo']}", entry['pagina'], mod_str
            ))
        
        # Atualizar tabela de Processos
        self.tree_proc.delete(*self.tree_proc.get_children())
        for proc in estado['processos']:
            self.tree_proc.insert('', 'end', values=(
                f"P{proc['id']}", proc['estado'], proc['tamanho'], proc['paginas']
            ))
        
        # Atualizar estatísticas da TLB
        stats = estado['estatisticas']
        if stats:
            self.label_acertos.config(text=f"Acertos: {stats.get('acertos', 0)}")
            self.label_falhas.config(text=f"Falhas: {stats.get('falhas', 0)}")
            self.label_taxa.config(text=f"Taxa de Acerto: {stats.get('taxaAcertos', 0):.1f}%")
        
        # Atualizar estado dos botões de navegação
        self.btn_voltar.config(state='normal' if self.ciclo_atual > 0 else 'disabled')
        self.btn_avancar.config(state='normal' if self.ciclo_atual < len(self.historico_completo) - 1 else 'disabled')
    
    def reset_simulacao(self):
        """Reseta completamente a simulação"""
        # Resetar variáveis do sistema
        self.mp = None
        self.tlb = None
        self.processos_lista = []
        self.historico_completo = []
        self.ciclo_atual = 0
        self.simulacao_executada = False
        
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
        
        # Desabilitar botões de navegação
        self.btn_voltar.config(state='disabled')
        self.btn_avancar.config(state='disabled')
        
        messagebox.showinfo("Reset", "Simulação resetada com sucesso!")

