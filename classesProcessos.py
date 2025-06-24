import math
from config import TAMANHO_PAGINA

# TODO: Definir uma forma de escolher o tamanho da página 
# (O ideal é que possa ser facilmente trocada a cada execução) (Passar como input?)
# E onde isso vai ficar no código
# OBS: Sempre que escrever alguma constante, escrever em letra maiúscula

class Processo:
    def __init__(self, id, tamanho):
        self.id = id
        # Possíveis estados:
        #   N = Novo
        #   E = Executando
        #   F = Finalizado
        #   P = Pronto
        #   B = Bloqueado
        #   PS = Pronto-Suspenso
        #   BS = Bloqueado-Suspenso
        self.estado = "N"
        self.tamanho = tamanho
        # Queremos sempre arredondar o número de páginas para cima
        # no comum caso de um valor não divisível de páginas
        self.quantidadePaginas = math.ceil(self.tamanho/TAMANHO_PAGINA)
        self.tabelaPaginas = TabelaPaginas(self.quantidadePaginas, id)


# TODO: Pensar estrutura da tabela de paginas

class TabelaPaginas:
    def __init__(self, quantidadePaginas, idProcesso):
        self.idProcesso = idProcesso
        self.quantidadeEntradas = quantidadePaginas
    self.entradas = [EntradaTP(idProcesso, i) for i in range(self.quantidadeEntradas)]

    def traduzirEndereco(self, enderecoVirtual, tlb=None):
        """
        Traduz um endereço virtual para físico usando a TLB (se disponível) e a tabela de páginas.
        
        Args:
            enderecoVirtual: Endereço virtual a ser traduzido
            tlb: Instância da TLB (opcional)
            
        Returns:
            tuple: (enderecoFisico, page_fault) onde:
                - enderecoFisico é o endereço físico traduzido
                - page_fault é True se ocorreu page fault, False caso contrário
        """
        # Calcula o número da página virtual e o offset
        numeroPaginaVirtual = enderecoVirtual // TAMANHO_PAGINA
        offset = enderecoVirtual % TAMANHO_PAGINA
        
        # Verifica se o VPN é válido
        if numeroPaginaVirtual >= self.quantidadeEntradas:
            raise ValueError(f"VPN {numeroPaginaVirtual} fora dos limites da tabela de páginas para o Processo {self.idProcesso}")
        
        # Se a TLB estiver disponível, tenta usar ela primeiro        
        if tlb:
            numeroFrameFisico = tlb.buscar(self.idProcesso, numeroPaginaVirtual)
            if numeroFrameFisico is not None:
                # TLB hit - retorna o endereço físico
                return (numeroFrameFisico * TAMANHO_PAGINA + offset, False)

        # TLB miss - consulta a tabela de páginas
        entrada = self.entradas[numeroPaginaVirtual]
        if not entrada.bitPresenca:
            # Page fault - página não está na memória
            return (None, True)
        
        # Página encontrada na tabela de páginas
        numeroFrameFisico = entrada.enderecoMemoriaPrincipal
        
        # Se houve TLB miss mas a página está na memória, o main irá inserir na TLB.
        
        # Retorna o endereço físico
        return (numeroFrameFisico * TAMANHO_PAGINA + offset, False)

class EntradaTP:
    def __init__(self, idProcesso, idEntrada):
        self.bitPresenca = False  # Indica se a página está na memória física
        self.bitModificacao = False  # Indica se a página foi modificada
        self.enderecoMemoriaPrincipal = None  # Número do frame físico (PFN)
        self.idProcesso = idProcesso

        # Ainda pensando se idEntrada pode ser utilizado em algum momento, deixar aqui...
        self.idEntrada = idEntrada
        
        self.pagina = Pagina(idProcesso, idEntrada)


class Pagina:
    def __init__(self, idProcesso, idPagina):
        self.idProcesso = idProcesso

        # Ainda pensando se idPagina pode ser utilizado em algum momento, deixar aqui...
        self.idPagina = idPagina

        self.dados = bytearray(TAMANHO_PAGINA)  # Dados da página
        self.referenciada = False  # Bit de referência para algoritmos de substituição
        self.modificada = False  # Bit de modificação