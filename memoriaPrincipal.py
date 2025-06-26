import collections
from config import NUM_QUADROS_MEMORIA_PRINCIPAL, POLITICA_SUB, PoliticaSubstituicao
from classesProcessos import Processo, Pagina

'''
IMPORTANTE:

    Verificar as alterações de processo.estado em próximas versões
    Uma página pode ser carregada para MP mas esse processo estar bloqueado?

'''

class Quadro:
    """
    Representa um quadro (frame) na memória principal.
    Um quadro pode conter uma página de um processo.
    """
    def __init__(self, id_quadro: int):
        self.id_quadro = id_quadro
        self.ocupado = False
        self.pagina: Pagina | None = None  # A página atualmente no quadro
        # Bit de 'uso' para o algoritmo do Relógio
        self.bit_utilizado = False

class MemoriaPrincipal:
    """
    Simula a memória principal (RAM) do sistema.
    É dividida em um número fixo de quadros.
    """
    def __init__(self):
        # Cria a lista de quadros (frames) da memória com base na configuração
        self.quadros = [Quadro(i) for i in range(NUM_QUADROS_MEMORIA_PRINCIPAL)]
        self.num_quadros_livres = NUM_QUADROS_MEMORIA_PRINCIPAL

        # Estruturas de dados para as políticas de substituição
        # Para LRU, usamos um deque que funciona como uma fila ordenada por uso
        self.quadros_refs_lru = collections.deque()
        # Para o Relógio, usamos um ponteiro que circula pelos quadros
        self.ponteiro_relogio = 0

    def encontrar_quadro_livre(self) -> Quadro | None:
        """
        Busca por um quadro que não esteja ocupado na memória principal.
        Retorna o primeiro quadro livre encontrado ou None se não houver nenhum.
        """
        if self.num_quadros_livres > 0:
            for quadro in self.quadros:
                if not quadro.ocupado:
                    return quadro
        return None

    def _substituicao_lru(self) -> Quadro:
        """
        Política de substituição LRU (Least Recently Used).
        Retorna o quadro que foi acessado menos recentemente.
        """
        # O quadro menos recentemente usado está no início do deque (à esquerda).
        quadro_a_substituir = self.quadros_refs_lru.popleft()
        print(f"Substituição LRU: Quadro {quadro_a_substituir.id_quadro} (P{quadro_a_substituir.pagina.id_processo}) foi o menos recentemente usado.")
        return quadro_a_substituir

    def _substituicao_relogio(self) -> Quadro:
        """
        Política de substituição do Relógio (Second-Chance).
        Procura por um quadro com bit de uso = 0 para substituir.
        """
        while True:
            quadro_atual = self.quadros[self.ponteiro_relogio]
            
            if not quadro_atual.bit_utilizado:
                # Encontrou um quadro para substituir (bit de uso é 0).
                print(f"Substituição Relógio: Quadro {quadro_atual.id_quadro} (bit uso=0) será substituído.")
                # Avança o ponteiro para a próxima posição para a próxima busca.
                self.ponteiro_relogio = (self.ponteiro_relogio + 1) % len(self.quadros)
                return quadro_atual
            else:
                # Dá uma segunda chance: zera o bit de uso e avança o ponteiro.
                quadro_atual.bit_utilizado = False
                print(f"Substituição Relógio: Dando segunda chance ao quadro {quadro_atual.id_quadro} (bit uso=1 -> 0).")
                self.ponteiro_relogio = (self.ponteiro_relogio + 1) % len(self.quadros)

    def _selecionar_quadro_para_substituicao(self) -> Quadro:
        """
        Seleciona um quadro para ser substituído com base na política configurada.
        """
        print(f"Memória cheia! Acionando política de substituição: {POLITICA_SUB.value}")
        if POLITICA_SUB == PoliticaSubstituicao.LRU:
            return self._substituicao_lru()
        elif POLITICA_SUB == PoliticaSubstituicao.RELOGIO:
            return self._substituicao_relogio()
        else:
            # Fallback - não deve acontecer com a validação em config.py
            raise NotImplementedError("Política de substituição não implementada.")

    def carrega_pagina(self, processo: Processo, pagina: Pagina) -> tuple[Quadro, Pagina | None]:
        """
        Aloca um quadro para uma página, trazendo-a para a memória principal.
        Se a memória estiver cheia, executa uma política de substituição.
        Retorna o quadro alocado e a página que foi substituída (se houver).
        """
        quadro_alocado = self.encontrar_quadro_livre()
        pagina_substituida = None

        if quadro_alocado:
            # Caso 1: Existe um quadro livre.
            print(f"Memória: Quadro livre {quadro_alocado.id_quadro} encontrado.")
            self.num_quadros_livres -= 1
        else:
            # Caso 2: Memória cheia, precisa substituir uma página.
            quadro_alocado = self._selecionar_quadro_para_substituicao()
            pagina_substituida = quadro_alocado.pagina

            # Se a página a ser substituída foi modificada, "salva em disco".
            if pagina_substituida and pagina_substituida.modificada:
                print(f"--- I/O (Disco) ---: Página {pagina_substituida.id_pagina} de P{pagina_substituida.id_processo} foi modificada. Salvando no disco...")
            
            # Invalida os dados da página antiga no quadro.
            if pagina_substituida:
                pagina_substituida.presente = False
                pagina_substituida.quadro_mp = -1

        # Aloca a nova página no quadro selecionado.
        quadro_alocado.ocupado = True
        quadro_alocado.pagina = pagina
        quadro_alocado.bit_utilizado = True # Marcado como usado na carga

        pagina.presente = True
        pagina.quadro_mp = quadro_alocado.id_quadro
        pagina.referenciada = True

        # Atualiza a lista LRU com o novo quadro como o mais recentemente usado.
        if quadro_alocado in self.quadros_refs_lru:
            self.quadros_refs_lru.remove(quadro_alocado)
        self.quadros_refs_lru.append(quadro_alocado)
        
        return quadro_alocado, pagina_substituida

    def writeBack(self, pagina):
        print(f"Write-back: Salvando página {pagina.idPagina} do processo P{pagina.idProcesso} no disco")