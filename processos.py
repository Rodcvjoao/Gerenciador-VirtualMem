import math

#TODO: Definir uma forma de escolher o tamanho da página
#E onde isso vai ficar no código
#OBS: Sempre que escrever alguma constante, escrever em letra maiúscula
TAM_PAGINA = 2**20

class Processo:
    def __init__(self, id, tamanho):
        self.id = id
        self.estado = "N"
        self.tamanho = tamanho
        self.qtdPaginas = math.ceil(self.tamanho/TAM_PAGINA)