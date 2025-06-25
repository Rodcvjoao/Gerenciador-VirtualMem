from collections import OrderedDict
from config import TAMANHO_TLB

class EntradaTLB:
    def __init__(self, numeroPaginaVirtual, numeroFrameFisico, idProcesso):
        self.numeroPaginaVirtual = numeroPaginaVirtual
        self.numeroFrameFisico = numeroFrameFisico
        self.idProcesso = idProcesso
        self.valido = True

class TLB:
    def __init__(self, tamanho=None):
        self.tamanho = tamanho if tamanho is not None else TAMANHO_TLB
        self.entradas = OrderedDict()
        self.acertos = 0
        self.falhas = 0

    def buscar(self, idProcesso, numeroPaginaVirtual):
        chave = (idProcesso, numeroPaginaVirtual)
        if chave in self.entradas:
            self.entradas.move_to_end(chave) # LRU: Mover para o fim (mais recente)
            self.acertos += 1
            return self.entradas[chave].numeroFrameFisico
        self.falhas += 1
        return None

    def inserir(self, idProcesso, numeroPaginaVirtual, numeroFrameFisico):
        chave = (idProcesso, numeroPaginaVirtual)
        if chave in self.entradas:
            self.entradas.pop(chave)
        elif len(self.entradas) >= self.tamanho:
            self.entradas.popitem(last=False)
        
        self.entradas[chave] = EntradaTLB(numeroPaginaVirtual, numeroFrameFisico, idProcesso)

    def invalidar_tudo(self):
        """Invalida todas as entradas da TLB, limpando completamente a estrutura."""
        self.entradas.clear()
        print("TLB: Todas as entradas foram invalidadas!")

   
    def invalidar_entrada(self, idProcesso, numeroPaginaVirtual):
        """
        Invalida uma entrada específica da TLB (usado em substituição de página).
        """
        chave = (idProcesso, numeroPaginaVirtual)
        if chave in self.entradas:
            del self.entradas[chave]

    def invalidar_processo(self, idProcesso):
        """
        Invalida todas as entradas de um processo específico (usado ao terminar um processo).
        """
        # Cria uma lista de chaves para remover para não modificar o dicionário enquanto itera
        chaves_para_remover = [k for k in self.entradas if k[0] == idProcesso]
        for chave in chaves_para_remover:
            del self.entradas[chave]
            print(f"TLB: Entrada {chave} invalidada.")

    


    def obterEstatisticas(self):
        total = self.acertos + self.falhas
        taxaAcertos = (self.acertos / total * 100) if total > 0 else 0
        return {
            'acertos': self.acertos,
            'falhas': self.falhas,
            'total': total,
            'taxaAcertos': taxaAcertos
        }

    def print_estado(self):
        print("\n--- Estado da TLB ---")
        if not self.entradas:
            print("  TLB está vazia.")
        else:
            print("  [ID Proc, VPN] -> PFN")
            for (idProc, vpn), entrada in self.entradas.items():
                print(f"  [{idProc}, {vpn}] -> {entrada.numeroFrameFisico}")
        
        stats = self.obterEstatisticas()
        print(f"  Estatísticas: {stats['acertos']} acertos, {stats['falhas']} falhas | Taxa de Acerto: {stats['taxaAcertos']:.2f}%")