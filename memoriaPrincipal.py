TAM_MEMORIA = 2**30
TAM_PAGINA = 2**20

class MemoriaPrincipal:
    # Por padrão, passaremos um valor base como o tamanho da memória principal
    def __init__(self, tamanho=TAM_MEMORIA):
        self.tamanho = tamanho
        self.quadros = [Quadro(i) for i in range(tamanho//TAM_PAGINA)]

class Quadro:
    def __init__(self, indiceQuadro):
        self.enderecoFisico = TAM_PAGINA * indiceQuadro
        self.processo = None