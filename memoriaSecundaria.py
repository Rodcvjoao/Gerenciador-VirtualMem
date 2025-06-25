class MemoriaSecundaria:
    def __init__(self, tamanho):
        self.swaps = {}
        self.tamanho = tamanho

# FIXME: REVER ESSA IMPLEMENTAÇÃO
'''
    def swap(self, pagina):
        self.paginasSuspensas.append(pagina)

    def swapProcesso(self, processo, memoriaPrincipal):
        processo.estado = "BS"
        # Adiciona as páginas do processo na memória secundária
        for entrada in processo.tabelaPaginas.entradas:
            self.swap(entrada.pagina)

            endMP = entrada.enderecoMemoriaPrincipal

            memoriaPrincipal.quadros[endMP].pagina = None
'''
            
class Swap:
    def __init__(self, processo):
        self.tamanho = processo.tamanho
        self.idProcessoSuspenso = processo.id
        self.paginasSuspensas = {}

        listaEntradas = processo.tabelaPaginas.entradas
        for i in range(len(listaEntradas)):
            self.paginasSuspensas[f"Página-{listaEntradas[i].idEntrada}"] = None
