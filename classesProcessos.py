import math

# TODO: Definir uma forma de escolher o tamanho da página 
# (O ideal é que possa ser facilmente trocada a cada execução) (Passar como input?)
# E onde isso vai ficar no código
# OBS: Sempre que escrever alguma constante, escrever em letra maiúscula
TAM_PAGINA = 2**20

class Processo:
    def __init__(self, id, tamanho):
        self.id = id
        self.estado = "N"
        self.tamanho = tamanho
        # Queremos sempre arredondar o número de páginas para cima
        # no comum caso de um valor não divisível de páginas
        self.qtdPaginas = math.ceil(self.tamanho/TAM_PAGINA)


# TODO: Pensar estrutura da tabela de paginas

class TabelaPagina:
    def __init__(self, qtdPaginas):
        self.qtdEntradas = qtdPaginas
        self.entradas = [EntradaTP() for i in range(self.qtdEntradas)]

class EntradaTP:
    def __init__(self):
        self.bitPresenca = False
        self.bitModificacao = False
        self.enderecoMP = None


class Pagina:
    pass