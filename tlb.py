from collections import OrderedDict
from config import TAMANHO_TLB

class EntradaTLB:
    def __init__(self, numeroPaginaVirtual, numeroFrameFisico, idProcesso):
        self.numeroPaginaVirtual = numeroPaginaVirtual  # Número da Página Virtual
        self.numeroFrameFisico = numeroFrameFisico  # Número do Frame Físico
        self.idProcesso = idProcesso  # ID do Processo
        self.valido = True

class TLB:
    def __init__(self, tamanho=None):
        # Usa o tamanho do arquivo de configuração se não for especificado
        self.tamanho = tamanho if tamanho is not None else TAMANHO_TLB
        # Usando OrderedDict para implementar a política de substituição LRU
        # O parâmetro tamanho determina quantas entradas a TLB pode armazenar
        self.entradas = OrderedDict()  # Chave: (idProcesso, numeroPaginaVirtual), Valor: EntradaTLB
        self.acertos = 0
        self.falhas = 0

    def buscar(self, idProcesso, numeroPaginaVirtual):
        """
        Procura um número de página virtual na TLB.
        Retorna o número do frame físico se encontrado, None caso contrário.
        """
        chave = (idProcesso, numeroPaginaVirtual)
        if chave in self.entradas:
            # Move a entrada para o final (mais recentemente usada)
            entrada = self.entradas.pop(chave)
            self.entradas[chave] = entrada
            self.acertos += 1
            return entrada.numeroFrameFisico
        self.falhas += 1
        return None

    def inserir(self, idProcesso, numeroPaginaVirtual, numeroFrameFisico):
        """
        Insere uma nova tradução na TLB.
        Se a TLB estiver cheia, a entrada menos recentemente usada é removida.
        """
        chave = (idProcesso, numeroPaginaVirtual)
        # Se a entrada já existe, atualiza ela
        if chave in self.entradas:
            self.entradas.pop(chave)
        
        # Se a TLB estiver cheia, remove a entrada menos recentemente usada
        if len(self.entradas) >= self.tamanho:
            self.entradas.popitem(last=False)  # Remove o primeiro item (mais antigo)
        
        # Adiciona a nova entrada
        self.entradas[chave] = EntradaTLB(numeroPaginaVirtual, numeroFrameFisico, idProcesso)

    def invalidar(self):
        """
        Invalida entradas da TLB.
        """
        self.entradas.clear()
        

    def obterEstatisticas(self):
        """
        Retorna estatísticas de acertos e falhas da TLB.
        """
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
            print("  [ID Processo, VPN] -> PFN")
            for (idProc, vpn), entrada in self.entradas.items():
                print(f"  [{idProc}, {vpn}] -> {entrada.numeroFrameFisico}")
        
        # Imprime as estatísticas
        stats = self.obterEstatisticas()
        print(f"  Estatísticas: {stats['acertos']} acertos, {stats['falhas']} falhas | Taxa de Acerto: {stats['taxaAcertos']:.2f}%")