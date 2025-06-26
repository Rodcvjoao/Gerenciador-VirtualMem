from collections import deque
from config import NUMERO_LINHAS_TLB

class EntradaTLB:
    """
    Representa uma única entrada na Translation Lookaside Buffer (TLB).
    Armazena um mapeamento de página virtual para quadro físico para um processo.
    """
    def __init__(self, id_processo: int, num_pagina_virtual: int, num_quadro: int):
        self.id_processo = id_processo
        self.num_pagina_virtual = num_pagina_virtual
        self.num_quadro = num_quadro

class TLB:
    """
    Implementa a Translation Lookaside Buffer (TLB), um cache para traduções de endereço.
    Utiliza uma política de substituição FIFO (First-In, First-Out).
    """
    def __init__(self):
        # A capacidade da TLB é definida no arquivo de configuração.
        self.capacidade = NUMERO_LINHAS_TLB
        # Usamos um 'deque' como uma fila para gerenciar as entradas da TLB de forma eficiente.
        self.entradas = deque(maxlen=self.capacidade)
        # Contadores para estatísticas de desempenho.
        self.hits = 0
        self.misses = 0

    def consultar(self, id_processo: int, num_pagina_virtual: int) -> int | None:
        """
        Consulta a TLB para encontrar um quadro físico para uma dada página virtual de um processo.
        Retorna o número do quadro se encontrado (TLB hit), ou None caso contrário (TLB miss).
        """
        for entrada in self.entradas:
            if entrada.id_processo == id_processo and entrada.num_pagina_virtual == num_pagina_virtual:
                return entrada.num_quadro
        return None

    def inserir(self, id_processo: int, num_pagina_virtual: int, num_quadro: int):
        """
        Insere uma nova tradução na TLB.
        Se a TLB estiver cheia, a entrada mais antiga (FIFO) é removida.
        """
        # Verifica se a entrada já existe para evitar duplicatas.
        for entrada in self.entradas:
            if entrada.id_processo == id_processo and entrada.num_pagina_virtual == num_pagina_virtual:
                # Se já existe, move para o final para uma política LRU, ou simplesmente retorna para FIFO.
                # Para FIFO, não fazemos nada se já existir. Se quiser LRU na TLB, precisa mover.
                return

        nova_entrada = EntradaTLB(id_processo, num_pagina_virtual, num_quadro)
        
        # O deque com maxlen=N remove automaticamente o item mais antigo quando está cheio.
        self.entradas.append(nova_entrada)

    def invalidar_processo(self, id_processo: int):
        """
        Remove todas as entradas da TLB associadas a um processo que foi finalizado.
        """
        # Cria uma nova lista contendo apenas as entradas que NÃO pertencem ao processo invalidado.
        entradas_a_manter = [e for e in self.entradas if e.id_processo != id_processo]
        self.entradas = deque(entradas_a_manter, maxlen=self.capacidade)
        print(f"TLB: Entradas do processo P{id_processo} invalidadas.")

    def invalidar_entrada(self, id_processo: int, num_pagina_virtual: int):
        """
        Remove uma entrada específica da TLB. Usado quando uma página é substituída na memória principal.
        """
        entrada_para_remover = None
        for entrada in self.entradas:
            if entrada.id_processo == id_processo and entrada.num_pagina_virtual == num_pagina_virtual:
                entrada_para_remover = entrada
                break
        
        if entrada_para_remover:
            self.entradas.remove(entrada_para_remover)

    def print_estado(self):
        """
        Imprime o estado atual da TLB, incluindo suas entradas e estatísticas.
        """
        print("\n--- Estado da TLB ---")
        if not self.entradas:
            print("  TLB está vazia.")
        else:
            print("  Entradas Atuais:")
            for i, entrada in enumerate(self.entradas):
                print(f"    [{i}] -> Processo P{entrada.id_processo}, Página {entrada.num_pagina_virtual} -> Quadro {entrada.num_quadro}")
        
        total_acessos = self.hits + self.misses
        taxa_hit = (self.hits / total_acessos * 100) if total_acessos > 0 else 0
        
        print("\n  Estatísticas:")
        print(f"    - Hits: {self.hits}")
        print(f"    - Misses: {self.misses}")
        print(f"    - Taxa de Acerto (Hit Rate): {taxa_hit:.2f}%")
        print("--------------------")