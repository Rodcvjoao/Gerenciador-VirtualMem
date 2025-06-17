TAM_MEMORIA = 2**30
TAM_PAGINA = 2**20

'''
IMPORTANTE:

    Verificar as alterações de processo.estado em próximas versões
    Uma página pode ser carregada para MP mas esse processo estar bloqueado?

'''

class MemoriaPrincipal:
    # Por padrão, passaremos um valor base como o tamanho da memória principal
    def __init__(self, tamanho=TAM_MEMORIA):
        self.tamanho = tamanho
        self.quadros = [Quadro(i) for i in range(tamanho//TAM_PAGINA)]

    # Usaremos essa função apenas na primeira vez que trouxermos o processo pra MP
    # A função TENTA alocar quadros da MP para o processo e troca o estado do processo para pronto caso consiga
    def carregaProcesso(self, processo):
        entradasVazias = [e for e in processo.tabelaPagina.entradas if not e.bitPresenca]
        indiceEV = 0
        i = 0
        while i < len(self.quadros) and indiceEV < len(entradasVazias):
            if self.quadros[i].pagina == None:
                self.quadros[i].pagina = entradasVazias[indiceEV].pagina
                self.quadros[i].bitUtilizado = True
                indiceEV += 1

            i += 1
        
        processo.estado = "P" if indiceEV > 0 else processo.estado

    def carregaPagina(self, processo, pagina):
        for q in self.quadros:
            if q.pagina == None:
                q.pagina = pagina
                q.bitUtilizado = True
                processo.estado = "P"
                return
            
        # TODO: Decidir como escolher a política de substituição (Arquivo config.py?)
        self.substituicaoLRU()
        self.substituicaoRelogio()
        
    
    def substituicaoLRU():
        # TODO: desenvolver política
        pass

    def substituicaoRelogio():
        # TODO: desenvolver política
        pass

class Quadro:
    def __init__(self, indiceQuadro):
        self.enderecoFisico = TAM_PAGINA * indiceQuadro
        self.pagina = None
        self.bitUtilizado = False