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

# - fiz a Refatoraão de memoriaPrincipal.py para retornar o quadro alocado
# Precisamos que as funções que alocam um quadro o retornem para o chamador.

    def carregaPagina(self, processo, pagina):
        # Primeiro, verifica se há quadros livres
        for q in self.quadros:
            if q.pagina == None:
                q.pagina = pagina
                q.bitUtilizado = True
                if q not in self.quadrosRefsLRU:
                    self.quadrosRefsLRU.append(q)
                
                # Retorna o quadro que acabou de ser alocado
                return q
            
        # Se não há quadros livres, chama a política de substituição
        print("Nenhum quadro livre. Acionando política de substituição.")
        quadro_substituido = None
        match POLITICA_SUB:
            case PoliticaSub.LRU.value:
                quadro_substituido = self.substituicaoLRU(pagina)
            case PoliticaSub.Relogio.value:
                quadro_substituido = self.substituicaoRelogio(pagina)
        
        return quadro_substituido
        
    def substituicaoLRU(self, pagina_nova):
        # O quadro a ser removido é o menos recentemente usado (o primeiro da lista)
        quadroEscolhido = self.quadrosRefsLRU.pop(0)
        pagina_antiga = quadroEscolhido.pagina

        print(f"Substituição LRU: Sai P{pagina_antiga.idProcesso}(Página {pagina_antiga.idPagina}), Entra P{pagina_nova.idProcesso}(Página {pagina_nova.idPagina}) no Quadro {quadroEscolhido.idQuadro}")

        if pagina_antiga.modificada:
            # Pagina presente no quadro vai para memória secundária
            self.writeBack(pagina_antiga)

        # Coloca a nova página no quadro
        quadroEscolhido.pagina = pagina_nova
        # O quadro escolhido agora é o mais recentemente usado
        self.quadrosRefsLRU.append(quadroEscolhido)

        return quadroEscolhido

    def substituicaoRelogio(self, pagina_nova):
        while True:
            quadroAtual = self.quadros[self.nextFrameRelogio % self.quantidadeQuadros]
            
            if not quadroAtual.bitUtilizado:
                # Encontrou um quadro para substituir
                pagina_antiga = quadroAtual.pagina
                print(f"Substituição Relógio: Sai P{pagina_antiga.idProcesso}(Página {pagina_antiga.idPagina}), Entra P{pagina_nova.idProcesso}(Página {pagina_nova.idPagina}) no Quadro {quadroAtual.idQuadro}")

                if pagina_antiga.modificada:
                    self.writeBack(pagina_antiga)
                
                quadroAtual.pagina = pagina_nova
                quadroAtual.bitUtilizado = True
                self.nextFrameRelogio = (self.nextFrameRelogio + 1) % self.quantidadeQuadros
                return quadroAtual
            else:
                # Dá uma segunda chance
                quadroAtual.bitUtilizado = False
                self.nextFrameRelogio = (self.nextFrameRelogio + 1) % self.quantidadeQuadros

    def writeBack(self, pagina):
        print(f"WRITE-BACK: Salvando página {pagina.idPagina} do processo P{pagina.idProcesso} na memória secundária.")
        # Lógica de escrita em disco (simulada)
        pagina.modificada = False # Reseta o bit M
        pass

#fim da mudança 1
class Quadro:
    def __init__(self, indiceQuadro):
        self.idQuadro = indiceQuadro
        self.enderecoFisico = TAMANHO_PAGINA * indiceQuadro
        self.pagina = None
        self.bitUtilizado = False