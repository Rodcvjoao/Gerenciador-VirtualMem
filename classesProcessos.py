import math
from config import TAMANHO_PAGINA_QUADRO_BYTES, TAMANHO_ENDERECO_LOGICO_BITS, BITS_OFFSET
from tlb import TLB

# TODO: Definir uma forma de escolher o tamanho da página 
# (O ideal é que possa ser facilmente trocada a cada execução) (Passar como input?)
# E onde isso vai ficar no código
# OBS: Sempre que escrever alguma constante, escrever em letra maiúscula

class Processo:
    """
    Representa um processo no sistema operacional simulado.
    """
    def __init__(self, id_processo: int, tamanho_bytes: int):
        if tamanho_bytes <= 0:
            raise ValueError("O tamanho do processo deve ser maior que zero.")

        self.id = id_processo
        self.tamanho_bytes = tamanho_bytes
        # Calcula quantas páginas são necessárias para o processo
        self.quantidade_paginas = math.ceil(tamanho_bytes / TAMANHO_PAGINA_QUADRO_BYTES)
        
        # O espaço de endereçamento virtual do processo não pode exceder o limite do sistema
        max_paginas_sistema = 2**(TAMANHO_ENDERECO_LOGICO_BITS - BITS_OFFSET)
        if self.quantidade_paginas > max_paginas_sistema:
            raise ValueError(f"Processo P{self.id} é muito grande para o espaço de endereçamento de {TAMANHO_ENDERECO_LOGICO_BITS} bits.")
            
        # Inicializa a tabela de páginas para este processo
        self.tabela_paginas = TabelaPaginas(self.id, self.quantidade_paginas)
        
        # Estado do processo: N=Novo, P=Pronto, E=Executando, B=Bloqueado, F=Finalizado
        self.estado = "N"
        
        print(f"P{self.id}: Criado com {self.tamanho_bytes} bytes, necessitando de {self.quantidade_paginas} páginas.")

class Pagina:
    """
    Representa uma única página no espaço de endereçamento de um processo.
    """
    def __init__(self, id_processo: int, id_pagina: int):
        self.id_processo = id_processo  # ID do processo ao qual a página pertence
        self.id_pagina = id_pagina      # ID da página (índice na tabela de páginas)
        self.modificada = False         # Bit M (Dirty Bit): True se a página foi alterada
        self.referenciada = False       # Bit R/U: True se a página foi referenciada recentemente
        self.presente = False           # Bit P: True se a página está na memória principal
        self.quadro_mp = -1             # Quadro da memória principal onde a página está alocada (-1 se não estiver)

class EntradaTabelaPaginas:
    """
    Representa uma entrada na Tabela de Páginas.
    Mapeia uma página virtual para um quadro físico.
    """
    def __init__(self, pagina: Pagina):
        self.pagina = pagina                          # A página associada a esta entrada
        self.bit_presenca = False                     # Bit P (Presente/Ausente)
        self.bit_modificacao = False                  # Bit M (Modificado/Dirty)
        self.endereco_quadro = -1                     # Endereço do quadro na memória principal

class TabelaPaginas:
    """
    Representa a Tabela de Páginas de um processo.
    Contém uma lista de entradas, uma para cada página do processo.
    """
    def __init__(self, id_processo: int, num_paginas: int):
        self.id_processo = id_processo
        # Cria a lista de páginas e as entradas correspondentes na tabela
        self.entradas = [EntradaTabelaPaginas(Pagina(id_processo, i)) for i in range(num_paginas)]
        self.num_paginas = num_paginas

    def traduzir_endereco(self, endereco_virtual: int, tlb: TLB):
        """
        Tenta traduzir um endereço virtual para um endereço físico.
        Primeiro, consulta a TLB. Se falhar (TLB miss), consulta a tabela de páginas.
        Retorna o endereço físico e um booleano indicando se houve page fault.
        """
        num_pagina = endereco_virtual // TAMANHO_PAGINA_QUADRO_BYTES
        offset = endereco_virtual % TAMANHO_PAGINA_QUADRO_BYTES

        # 1. Tenta encontrar a tradução na TLB (TLB Hit/Miss)
        resultado_tlb = tlb.consultar(self.id_processo, num_pagina)
        
        if resultado_tlb is not None:
            # TLB Hit: Endereço encontrado na TLB
            tlb.hits += 1
            endereco_quadro = resultado_tlb
            endereco_fisico = endereco_quadro * TAMANHO_PAGINA_QUADRO_BYTES + offset
            print(f"P{self.id_processo}: TLB HIT! Página {num_pagina} -> Quadro {endereco_quadro}")
            return endereco_fisico, False  # False indica que não houve page fault
        
        # TLB Miss: Endereço não está na TLB
        tlb.misses += 1
        print(f"P{self.id_processo}: TLB MISS para página {num_pagina}. Consultando Tabela de Páginas.")

        # 2. Consulta a Tabela de Páginas
        if num_pagina >= len(self.entradas):
             # Este erro deve ser prevenido antes, mas é uma salvaguarda.
            print(f"ERRO: Tentativa de acesso a página {num_pagina} que não existe.")
            return -1, True

        entrada = self.entradas[num_pagina]

        if entrada.bit_presenca:
            # Page Hit: A página está na memória principal.
            endereco_quadro = entrada.endereco_quadro
            # Adiciona a nova tradução à TLB para acessos futuros
            tlb.inserir(self.id_processo, num_pagina, endereco_quadro)
            endereco_fisico = endereco_quadro * TAMANHO_PAGINA_QUADRO_BYTES + offset
            return endereco_fisico, False
        else:
            # Page Fault: A página não está na memória principal.
            return -1, True