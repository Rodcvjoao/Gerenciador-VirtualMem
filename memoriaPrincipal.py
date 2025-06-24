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

    def referenciar_quadro_lru(self, quadro):
        """
        Atualiza a posição de um quadro na lista do LRU, movendo-o para o final (mais recente).
        Isso deve ser chamado a cada acesso a uma página.
        """
        if quadro in self.quadrosRefsLRU:
            # Remove de sua posição atual
            self.quadrosRefsLRU.remove(quadro)
        # Adiciona no final da lista (mais recentemente usado)
        self.quadrosRefsLRU.append(quadro)


    def carregaPagina(self, processo, pagina_nova):
        # Primeiro, verifica se há quadros livres
        for q in self.quadros:
            if q.pagina is None:
                q.pagina = pagina_nova
                q.bitUtilizado = True
                # Apenas adiciona ao final, pois é o primeiro uso
                self.quadrosRefsLRU.append(q)
                return q, None # Retorna o quadro alocado e None (nenhuma página substituída
            
        # Se não há quadros livres, chama a política de substituição
        print("Nenhum quadro livre. Acionando política de substituição.")
        quadro_usado, pagina_antiga = None, None
        match POLITICA_SUB:
            case PoliticaSub.LRU.value:
                quadro_usado, pagina_antiga = self.substituicaoLRU(pagina_nova)
            case PoliticaSub.Relogio.value:
                quadro_usado, pagina_antiga = self.substituicaoRelogio(pagina_nova)
        
        return quadro_usado, pagina_antiga
        
    def substituicaoLRU(self, pagina_nova):
        quadroEscolhido = self.quadrosRefsLRU.pop(0)
        pagina_antiga = quadroEscolhido.pagina # Salva a referência da página antiga

        print(f"Substituição LRU: Sai P{pagina_antiga.idProcesso}(Página {pagina_antiga.idPagina}), Entra P{pagina_nova.idProcesso}(Página {pagina_nova.idPagina}) no Quadro {quadroEscolhido.idQuadro}")

        if pagina_antiga.modificada:
            self.writeBack(pagina_antiga)

        # Coloca a nova página no quadro
        quadroEscolhido.pagina = pagina_nova
        self.quadrosRefsLRU.append(quadroEscolhido)

        return quadroEscolhido, pagina_antiga # Retorna o quadro e a página que foi removida

    def substituicaoRelogio(self, pagina_nova):
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