import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class Tela_Simular:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Gerenciamento de Memória")
        self.root.geometry("800x800")
        self.root.configure(bg='#f0f0f0')
        
        # Dados da simulação
        self.ciclo_atual = 0
        self.comandos = []
        self.historico_tlb = {}
        self.historico_mem_principal = {}
        self.historico_mem_secundaria = {}
        self.historico_stats = {}
        self.endereco_virtual_atual = "0x0000"
        
        # Inicializar dados de exemplo
        self.inicializar_dados_exemplo()
        
        # Criar interface
        self.criar_interface()
        self.atualizar_interface()
    
    def inicializar_dados_exemplo(self):
        """Inicializa dados de exemplo para demonstração"""
        # Comandos de exemplo
        self.comandos = [
            "READ 0x1000",
            "WRITE 0x2000", 
            "READ 0x1500",
            "WRITE 0x3000"
        ]
        
        # Histórico de TLB para cada ciclo
        self.historico_tlb = {
            0: [("0x10", "0x100", "Valid"), ("0x20", "0x200", "Valid")],
            1: [("0x10", "0x100", "Valid"), ("0x20", "0x200", "Valid"), ("0x15", "0x150", "Valid")],
            2: [("0x10", "0x100", "Valid"), ("0x15", "0x150", "Valid"), ("0x30", "0x300", "Valid")],
            3: [("0x15", "0x150", "Valid"), ("0x30", "0x300", "Valid"), ("0x25", "0x250", "Valid")]
        }
        
        # Histórico de Memória Principal
        self.historico_mem_principal = {
            0: [("0x100", "0x1000", "RW"), ("0x200", "0x2000", "RW")],
            1: [("0x100", "0x1000", "RW"), ("0x200", "0x2000", "RW"), ("0x150", "0x1500", "R")],
            2: [("0x100", "0x1000", "RW"), ("0x150", "0x1500", "R"), ("0x300", "0x3000", "W")],
            3: [("0x150", "0x1500", "R"), ("0x300", "0x3000", "W"), ("0x250", "0x2500", "RW")]
        }
        
        # Histórico de Memória Secundária
        self.historico_mem_secundaria = {
            0: [("0x400", "Página A"), ("0x500", "Página B"), ("0x600", "Página C")],
            1: [("0x400", "Página A"), ("0x500", "Página B"), ("0x600", "Página C")],
            2: [("0x200", "Página D"), ("0x500", "Página B"), ("0x600", "Página C")],
            3: [("0x200", "Página D"), ("0x100", "Página E"), ("0x600", "Página C")]
        }
        
        # Histórico de estatísticas
        self.historico_stats = {
            0: {"acertos": 0, "faltas": 0, "endereco": "0x1000"},
            1: {"acertos": 1, "faltas": 0, "endereco": "0x2000"},
            2: {"acertos": 1, "faltas": 1, "endereco": "0x1500"},
            3: {"acertos": 2, "faltas": 1, "endereco": "0x3000"}
        }
    
    def criar_interface(self):
        """Cria todos os elementos da interface"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        titulo = tk.Label(main_frame, text="Simulador de Gerenciamento de Memória", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0')
        titulo.pack(pady=(0, 10))
        
        # Frame superior (controles e informações)
        top_frame = tk.Frame(main_frame, bg='#f0f0f0')
        top_frame.pack(fill='x', pady=(0, 10))
        
        # Botão carregar arquivo
        btn_carregar = tk.Button(top_frame, text="Carregar Arquivo", 
                               command=self.carregar_arquivo, 
                               font=('Arial', 10), bg='#e0e0e0')
        btn_carregar.pack(side='left', padx=(0, 10))
        
        # Informações do ciclo atual
        self.label_ciclo = tk.Label(top_frame, text=f"Ciclo: {self.ciclo_atual}", 
                                   font=('Arial', 12, 'bold'), bg='#f0f0f0')
        self.label_ciclo.pack(side='left', padx=(0, 20))
        
        self.label_comando = tk.Label(top_frame, text="Comando atual: ", 
                                    font=('Arial', 10), bg='#f0f0f0')
        self.label_comando.pack(side='left', padx=(0, 20))
        
        self.label_endereco = tk.Label(top_frame, text="Endereço Virtual: ", 
                                     font=('Arial', 10), bg='#f0f0f0')
        self.label_endereco.pack(side='left')
        
        # Frame central (tabelas)
        central_frame = tk.Frame(main_frame, bg='#f0f0f0')
        central_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        # Frame esquerdo (TLB e Estatísticas)
        left_frame = tk.Frame(central_frame, bg='#f0f0f0')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        # TLB
        self.criar_tabela_tlb(left_frame)
        
        # Estatísticas
        self.criar_frame_estatisticas(left_frame)
        
        # Frame direito (Memórias)
        right_frame = tk.Frame(central_frame, bg='#f0f0f0')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))
        
        # Memória Principal
        self.criar_tabela_memoria_principal(right_frame)
        
        # Memória Secundária
        self.criar_tabela_memoria_secundaria(right_frame)
        
        # Frame inferior (botões de navegação)
        bottom_frame = tk.Frame(main_frame, bg='#f0f0f0')
        bottom_frame.pack(fill='x', pady=(10, 0))
        
        # Botões de navegação
        nav_frame = tk.Frame(bottom_frame, bg='#f0f0f0')
        nav_frame.pack()
        
        self.btn_voltar = tk.Button(nav_frame, text="◀ Voltar", 
                                   command=self.voltar_ciclo,
                                   font=('Arial', 12), bg='#d0d0d0', 
                                   width=10, height=2)
        self.btn_voltar.pack(side='left', padx=(0, 20))
        
        self.label_ciclo_nav = tk.Label(nav_frame, text=f"Ciclo {self.ciclo_atual}", 
                                       font=('Arial', 14, 'bold'), bg='#f0f0f0')
        self.label_ciclo_nav.pack(side='left', padx=20)
        
        self.btn_avancar = tk.Button(nav_frame, text="Avançar ▶", 
                                    command=self.avancar_ciclo,
                                    font=('Arial', 12), bg='#d0d0d0', 
                                    width=10, height=2)
        self.btn_avancar.pack(side='left', padx=(20, 0))
    
    def criar_tabela_tlb(self, parent):
        """Cria a tabela TLB"""
        frame_tlb = tk.LabelFrame(parent, text="TLB (Translation Lookaside Buffer)", 
                                 font=('Arial', 11, 'bold'), bg='#f0f0f0')
        frame_tlb.pack(fill='both', expand=True, pady=(0, 10))
        
        # Treeview para TLB
        self.tree_tlb = ttk.Treeview(frame_tlb, columns=('virtual', 'fisica', 'status'), 
                                    show='headings', height=6)
        
        self.tree_tlb.heading('virtual', text='Página Virtual')
        self.tree_tlb.heading('fisica', text='Página Física')
        self.tree_tlb.heading('status', text='Status')
        
        self.tree_tlb.column('virtual', width=120, anchor='center')
        self.tree_tlb.column('fisica', width=120, anchor='center')
        self.tree_tlb.column('status', width=100, anchor='center')
        
        # Scrollbar para TLB
        scrollbar_tlb = ttk.Scrollbar(frame_tlb, orient='vertical', command=self.tree_tlb.yview)
        self.tree_tlb.configure(yscrollcommand=scrollbar_tlb.set)
        
        self.tree_tlb.pack(side='left', fill='both', expand=True, padx=(5, 0), pady=5)
        scrollbar_tlb.pack(side='right', fill='y', pady=5)
    
    def criar_frame_estatisticas(self, parent):
        """Cria o frame de estatísticas"""
        frame_stats = tk.LabelFrame(parent, text="Estatísticas", 
                                   font=('Arial', 11, 'bold'), bg='#f0f0f0')
        frame_stats.pack(fill='x', pady=(0, 10))
        
        stats_content = tk.Frame(frame_stats, bg='#f0f0f0')
        stats_content.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.label_acertos = tk.Label(stats_content, text="Acertos: 0", 
                                     font=('Arial', 11), bg='#f0f0f0', fg='green')
        self.label_acertos.pack(anchor='w', pady=2)
        
        self.label_faltas = tk.Label(stats_content, text="Faltas de Página: 0", 
                                    font=('Arial', 11), bg='#f0f0f0', fg='red')
        self.label_faltas.pack(anchor='w', pady=2)
        
        self.label_taxa = tk.Label(stats_content, text="Taxa de Acerto: 0%", 
                                  font=('Arial', 11), bg='#f0f0f0', fg='blue')
        self.label_taxa.pack(anchor='w', pady=2)
    
    def criar_tabela_memoria_principal(self, parent):
        """Cria a tabela de Memória Principal"""
        frame_mp = tk.LabelFrame(parent, text="Memória Principal", 
                                font=('Arial', 11, 'bold'), bg='#f0f0f0')
        frame_mp.pack(fill='both', expand=True, pady=(0, 10))
        
        self.tree_mp = ttk.Treeview(frame_mp, columns=('frame', 'pagina', 'acesso'), 
                                   show='headings', height=6)
        
        self.tree_mp.heading('frame', text='Frame')
        self.tree_mp.heading('pagina', text='Página')
        self.tree_mp.heading('acesso', text='Acesso')
        
        self.tree_mp.column('frame', width=100, anchor='center')
        self.tree_mp.column('pagina', width=120, anchor='center')
        self.tree_mp.column('acesso', width=80, anchor='center')
        
        scrollbar_mp = ttk.Scrollbar(frame_mp, orient='vertical', command=self.tree_mp.yview)
        self.tree_mp.configure(yscrollcommand=scrollbar_mp.set)
        
        self.tree_mp.pack(side='left', fill='both', expand=True, padx=(5, 0), pady=5)
        scrollbar_mp.pack(side='right', fill='y', pady=5)
    
    def criar_tabela_memoria_secundaria(self, parent):
        """Cria a tabela de Memória Secundária"""
        frame_ms = tk.LabelFrame(parent, text="Memória Secundária", 
                                font=('Arial', 11, 'bold'), bg='#f0f0f0')
        frame_ms.pack(fill='both', expand=True)
        
        self.tree_ms = ttk.Treeview(frame_ms, columns=('endereco', 'conteudo'), 
                                   show='headings', height=6)
        
        self.tree_ms.heading('endereco', text='Endereço')
        self.tree_ms.heading('conteudo', text='Conteúdo')
        
        self.tree_ms.column('endereco', width=120, anchor='center')
        self.tree_ms.column('conteudo', width=180, anchor='center')
        
        scrollbar_ms = ttk.Scrollbar(frame_ms, orient='vertical', command=self.tree_ms.yview)
        self.tree_ms.configure(yscrollcommand=scrollbar_ms.set)
        
        self.tree_ms.pack(side='left', fill='both', expand=True, padx=(5, 0), pady=5)
        scrollbar_ms.pack(side='right', fill='y', pady=5)
    
    
    def voltar_ciclo(self):
        """Volta para o ciclo anterior"""
        if self.ciclo_atual > 0:
            self.ciclo_atual -= 1
            self.atualizar_interface()
    
    def avancar_ciclo(self):
        """Avança para o próximo ciclo"""
        max_ciclos = max(len(self.comandos) - 1, 3)  # Pelo menos 4 ciclos (0-3)
        if self.ciclo_atual < max_ciclos:
            self.ciclo_atual += 1
            self.atualizar_interface()
    
    def atualizar_interface(self):
        """Atualiza toda a interface com os dados do ciclo atual"""
        # Atualizar labels
        self.label_ciclo.config(text=f"Ciclo: {self.ciclo_atual}")
        self.label_ciclo_nav.config(text=f"Ciclo {self.ciclo_atual}")
        
        # Atualizar comando atual
        if self.ciclo_atual < len(self.comandos):
            comando_atual = self.comandos[self.ciclo_atual]
        else:
            comando_atual = "Nenhum comando"
        self.label_comando.config(text=f"Comando atual: {comando_atual}")
        
        # Atualizar endereço virtual
        stats = self.historico_stats.get(self.ciclo_atual, {"endereco": "0x0000"})
        self.label_endereco.config(text=f"Endereço Virtual: {stats['endereco']}")
        
        # Atualizar tabelas
        self.atualizar_tabela_tlb()
        self.atualizar_tabela_memoria_principal()
        self.atualizar_tabela_memoria_secundaria()
        
        # Atualizar estatísticas
        self.atualizar_estatisticas()
        
        # Atualizar estado dos botões
        self.btn_voltar.config(state='normal' if self.ciclo_atual > 0 else 'disabled')
        max_ciclos = max(len(self.comandos) - 1, 3)
        self.btn_avancar.config(state='normal' if self.ciclo_atual < max_ciclos else 'disabled')
    
    def atualizar_tabela_tlb(self):
        """Atualiza a tabela TLB"""
        # Limpar tabela
        for item in self.tree_tlb.get_children():
            self.tree_tlb.delete(item)
        
        # Adicionar dados do ciclo atual
        dados_tlb = self.historico_tlb.get(self.ciclo_atual, [])
        for virtual, fisica, status in dados_tlb:
            self.tree_tlb.insert('', 'end', values=(virtual, fisica, status))
    
    def atualizar_tabela_memoria_principal(self):
        """Atualiza a tabela de Memória Principal"""
        # Limpar tabela
        for item in self.tree_mp.get_children():
            self.tree_mp.delete(item)
        
        # Adicionar dados do ciclo atual
        dados_mp = self.historico_mem_principal.get(self.ciclo_atual, [])
        for frame, pagina, acesso in dados_mp:
            self.tree_mp.insert('', 'end', values=(frame, pagina, acesso))
    
    def atualizar_tabela_memoria_secundaria(self):
        """Atualiza a tabela de Memória Secundária"""
        # Limpar tabela
        for item in self.tree_ms.get_children():
            self.tree_ms.delete(item)
        
        # Adicionar dados do ciclo atual
        dados_ms = self.historico_mem_secundaria.get(self.ciclo_atual, [])
        for endereco, conteudo in dados_ms:
            self.tree_ms.insert('', 'end', values=(endereco, conteudo))
    
    def atualizar_estatisticas(self):
        """Atualiza as estatísticas"""
        stats = self.historico_stats.get(self.ciclo_atual, {"acertos": 0, "faltas": 0})
        
        acertos = stats["acertos"]
        faltas = stats["faltas"]
        total = acertos + faltas
        taxa = (acertos / total * 100) if total > 0 else 0
        
        self.label_acertos.config(text=f"Acertos: {acertos}")
        self.label_faltas.config(text=f"Faltas de Página: {faltas}")
        self.label_taxa.config(text=f"Taxa de Acerto: {taxa:.1f}%")

def main():
    root = tk.Tk()
    app = Tela_Simular(root)
    root.mainloop()

if __name__ == "__main__":
    main()