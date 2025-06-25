class MemoriaSecundaria:
    def __init__(self, tamanho):
        self.paginasSuspensas = []
        self.tamanho = tamanho
    
    def swap(self, pagina):
        self.paginasSuspensas.append(pagina)

    def swapProcesso(self, processo):
        processo.estado = "BS"
        for entrada in processo.tabelaPaginas.entradas:
            self.swap(entrada.pagina)

# TODO: Continuar implementação de MemoriaSecundaria
#       Entender como write back poderia funcionar, tratando das questões
#       de páginas em memSecundária e memPrincipal