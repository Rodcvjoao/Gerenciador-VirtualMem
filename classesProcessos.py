import math
from config import TAM_PAGINA

# TODO: Definir uma forma de escolher o tamanho da página 
# (O ideal é que possa ser facilmente trocada a cada execução) (Passar como input?)
# E onde isso vai ficar no código
# OBS: Sempre que escrever alguma constante, escrever em letra maiúscula

class Processo:
    def __init__(self, id, tamanho):
        self.id = id
        self.estado = "N"
        self.tamanho = tamanho
        # Queremos sempre arredondar o número de páginas para cima
        # no comum caso de um valor não divisível de páginas
        self.qtdPaginas = math.ceil(self.tamanho/TAM_PAGINA)
        self.tabelaPagina = TabelaPagina(self.qtdPaginas)


# TODO: Pensar estrutura da tabela de paginas

class TabelaPagina:
    def __init__(self, qtdPaginas):
        self.qtdEntradas = qtdPaginas
        self.entradas = [EntradaTP() for i in range(self.qtdEntradas)]
    
    def traduzir_endereco(self, endereco_virtual, tlb=None):
        """
        Traduz um endereço virtual para físico usando a TLB (se disponível) e a tabela de páginas.
        
        Args:
            endereco_virtual: Endereço virtual a ser traduzido
            tlb: Instância da TLB (opcional)
            
        Returns:
            tuple: (endereco_fisico, page_fault) onde:
                - endereco_fisico é o endereço físico traduzido
                - page_fault é True se ocorreu page fault, False caso contrário
        """
        # Calcula o número da página virtual e o offset
        vpn = endereco_virtual // TAM_PAGINA
        offset = endereco_virtual % TAM_PAGINA
        
        # Verifica se o VPN é válido
        if vpn >= self.qtdEntradas:
            raise ValueError(f"VPN {vpn} fora dos limites da tabela de páginas")
        
        # Se a TLB estiver disponível, tenta usar ela primeiro
        if tlb is not None:
            pfn = tlb.lookup(self.entradas[vpn].pid, vpn)
            if pfn is not None:
                # TLB hit - retorna o endereço físico
                return (pfn * TAM_PAGINA + offset, False)
        
        # TLB miss ou não disponível - consulta a tabela de páginas
        entrada = self.entradas[vpn]
        if not entrada.bitPresenca:
            # Page fault - página não está na memória
            return (None, True)
        
        # Página encontrada na tabela de páginas
        pfn = entrada.enderecoMP
        
        # Se a TLB estiver disponível, atualiza ela
        if tlb is not None:
            tlb.insert(entrada.pid, vpn, pfn)
        
        # Retorna o endereço físico
        return (pfn * TAM_PAGINA + offset, False)

class EntradaTP:
    def __init__(self):
        self.bitPresenca = False  # Indica se a página está na memória física
        self.bitModificacao = False  # Indica se a página foi modificada
        self.enderecoMP = None  # Número do frame físico (PFN)
        self.pid = None  # ID do processo dono da página

class Pagina:
    def __init__(self, pid, vpn):
        self.pid = pid
        self.vpn = vpn
        self.dados = bytearray(TAM_PAGINA)  # Dados da página
        self.referenciada = False  # Bit de referência para algoritmos de substituição
        self.modificada = False  # Bit de modificação