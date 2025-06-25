from config import *

'''
IMPORTANTE:

    Verificar as alterações de processo.estado em próximas versões
    Uma página pode ser carregada para MP mas esse processo estar bloqueado?

'''

class MemoriaPrincipal:
    # Por padrão, passaremos um valor base como o tamanho da memória principal
    def __init__(self, tamanho=TAMANHO_MEMORIA_P):
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

    def carregaPagina(self, processo, pagina_nova):
        # Primeiro, verifica se há quadros livres
        for q in self.quadros:
            if q.pagina is None:
                q.pagina = pagina_nova
                q.bitUtilizado = True
                if q in self.quadrosRefsLRU:
                    # Se esse quadro já tiver sido referenciado, retire da sua posição atual
                    # e coloque no fim da fila. (Na política LRU, ele foi o mais recentemente acessado)
                    self.quadrosRefsLRU.pop(self.quadrosRefsLRU.index(q))
                # Retorna o quadro alocado e None, pois nenhuma página foi substituída
                return q, None
            
        # Se não há quadros livres, chama a política de substituição
        print("Nenhum quadro livre. Acionando política de substituição.")
        quadro_usado, pagina_antiga = None, None
        match POLITICA_SUB:
            case PoliticaSub.LRU.value:
                quadro_usado, pagina_antiga = self.substituicaoLRU(pagina_nova)
            case PoliticaSub.Relogio.value:
                quadro_usado, pagina_antiga = self.substituicaoRelogio(pagina_nova)
        
        return quadro_usado, pagina_antiga
        
    def substituicaoLRU(self, pagina_nova, memoriaSecundaria):
        quadroEscolhido = self.quadrosRefsLRU.pop(0)
        pagina_antiga = quadroEscolhido.pagina # Salva a referência da página antiga

        # FIXME: Rever essa implementação de Swap
        #memoriaSecundaria.swap(pagina_antiga)

        print(f"Substituição LRU: Sai P{pagina_antiga.idProcesso}(Página {pagina_antiga.idPagina}), Entra P{pagina_nova.idProcesso}(Página {pagina_nova.idPagina}) no Quadro {quadroEscolhido.idQuadro}")

        if pagina_antiga.modificada:
            self.writeBack(pagina_antiga)

        # Coloca a nova página no quadro
        quadroEscolhido.pagina = pagina_nova
        self.quadrosRefsLRU.append(quadroEscolhido)

        return quadroEscolhido, pagina_antiga # Retorna o quadro e a página que foi removida

    def substituicaoRelogio(self, pagina_nova, memoriaSecundaria):
        while True:
            quadroAtual = self.quadros[self.nextFrameRelogio % self.quantidadeQuadros]
            
            if not quadroAtual.bitUtilizado:
                pagina_antiga = quadroAtual.pagina # Salva a referência
                print(f"Substituição Relógio: Sai P{pagina_antiga.idProcesso}(Página {pagina_antiga.idPagina}), Entra P{pagina_nova.idProcesso}(Página {pagina_nova.idPagina}) no Quadro {quadroAtual.idQuadro}")

                if pagina_antiga.modificada:
                    self.writeBack(pagina_antiga)
                
                quadroAtual.pagina = pagina_nova
                quadroAtual.bitUtilizado = True
                self.nextFrameRelogio = (self.nextFrameRelogio + 1) % self.quantidadeQuadros
                return quadroAtual, pagina_antiga # Retorna o quadro e a página removida
            else:
                quadroAtual.bitUtilizado = False
                self.nextFrameRelogio = (self.nextFrameRelogio + 1) % self.quantidadeQuadros
            self.nextFrameRelogio += 1

    def writeBack(self, pagina):
        pass

class Quadro:
    def __init__(self, indiceQuadro):
        self.idQuadro = indiceQuadro
        self.enderecoFisico = TAMANHO_PAGINA * indiceQuadro
        self.pagina = None
        self.bitUtilizado = False