import copy

class MemoriaSecundaria:
    def __init__(self, tamanho):
        self.swaps = {}
        self.tamanho = tamanho


    def swapPagina(self, pagina, processo):
        if self.swaps.get(processo.id) == None:
            self.swaps[processo.id] = Swap(processo)
        
        paginasSuspensas = self.swaps[pagina.idProcesso].paginasSuspensas
        if pagina.idPagina not in paginasSuspensas:
            paginasSuspensas[pagina.idPagina] = copy.copy(pagina)
            

    def swapProcesso(self, processo):
        if self.swaps.get(processo.id) == None:
            self.swaps[processo.id] = Swap(processo)

        for entrada in processo.tabelaPaginas.entradas:
            self.swapPagina(entrada.pagina, processo)
            
class Swap:
    def __init__(self, processo):
        self.tamanho = processo.tamanho
        self.idProcessoSuspenso = processo.id
        self.paginasSuspensas = {}

        listaEntradas = processo.tabelaPaginas.entradas
        for i in range(len(listaEntradas)):
            self.paginasSuspensas[listaEntradas[i].idEntrada] = None