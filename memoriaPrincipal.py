from config import *

'''
IMPORTANTE:

    Verificar as alterações de processo.estado em próximas versões
    Uma página pode ser carregada para MP mas esse processo estar bloqueado?

'''

class MemoriaPrincipal:
    # Por padrão, passaremos um valor base como o tamanho da memória principal
    def __init__(self, tamanho=TAMANHO_MEMORIA):
        self.tamanho = tamanho
        self.quantidadeQuadros = tamanho//TAMANHO_PAGINA
        self.quadros = [Quadro(i) for i in range(self.quantidadeQuadros)]

        # Faremos uma lista com todos os quadros que foram referenciados,
        # atualizando sua ordem conforme o mesmo quadro tiver sido referenciado mais de uma vez.
        # Essa lista não poderá passar do tamanho máximo de quadros
        # (suponha o caso em que toda a MP está cheia com páginas de processos
        # e uma nova página precisa ser acessada) portanto, o primeiro item da lista deve ser substituido
        self.quadrosRefsLRU = []
        self.nextFrameRelogio = 0

    # Usaremos essa função apenas na primeira vez que trouxermos o processo pra MP
    # A função TENTA alocar quadros da MP para o processo e troca o estado do processo para pronto caso consiga
    def carregaProcesso(self, processo):
        entradasVazias = [e for e in processo.tabelaPagina.entradas if not e.bitPresenca]
        indiceEV = 0
        i = 0
        while i < self.quantidadeQuadros and indiceEV < len(entradasVazias):
            if self.quadros[i].pagina == None:
                self.quadros[i].pagina = entradasVazias[indiceEV].pagina
                self.quadros[i].bitUtilizado = True
                self.quadrosRefsLRU.append(self.quadros[i])
                
                indiceEV += 1

            # CHECAR SE TODAS AS PÁGINAS FORAM APROPRIADAMENTE ALOCADAS
            # CASO CONTÁRIO, JOGAR PARA MEMÓRIA SECUNDÁRIA

            i += 1
        
        processo.estado = "P" if indiceEV > 0 else processo.estado

    def carregaPagina(self, processo, pagina):
        for q in self.quadros:
            if q.pagina == None:
                q.pagina = pagina
                q.bitUtilizado = True
                if q in self.quadrosRefsLRU:
                    # Se esse quadro já tiver sido referenciado, retire da sua posição atual
                    # e coloque no fim da fila. (Na política LRU, ele foi o mais recentemente acessado)
                    self.quadrosRefsLRU.pop(self.quadrosRefsLRU.index(q))
                    self.quadrosRefsLRU.append(q)

                # TODO: VERIFICAR SE ESSE PROCESSO NECESSARIAMENTE ESTARÁ COMO PRONTO
                processo.estado = "P"
                return
            
        match POLITICA_SUB:
            case PoliticaSub.LRU.value:
                self.substituicaoLRU(pagina)
            case PoliticaSub.Relogio.value:
                self.substituicaoRelogio(pagina)
        
    def substituicaoLRU(self, pagina):
        quadroRemovido = self.quadrosRefsLRU.pop(0)

        if quadroRemovido.pagina.modificada == True:
            # Pagina presente no quadro vai para memória secundária
            self.writeBack(quadroRemovido.pagina)

        quadroRemovido.pagina = pagina
        self.quadrosRefsLRU.append(quadroRemovido)

    def substituicaoRelogio(self, pagina):
        while True:
            quadroAnalisado = self.nextFrameRelogio % self.quantidadeQuadros
            if self.quadros[quadroAnalisado].bitUtilizado == False:
                if self.quadros[quadroAnalisado].pagina.modificada == True:
                    self.writeBack(self.quadros[quadroAnalisado].pagina)
                
                self.quadros[quadroAnalisado].pagina = pagina
                self.quadros[quadroAnalisado].bitUtilizado = True
            else:
                self.quadros[quadroAnalisado].bitUtilizado = False

            self.nextFrameRelogio += 1

    def writeBack(self, pagina):
        pass

class Quadro:
    def __init__(self, indiceQuadro):
        self.idQuadro = indiceQuadro
        self.enderecoFisico = TAMANHO_PAGINA * indiceQuadro
        self.pagina = None
        self.bitUtilizado = False