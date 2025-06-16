from collections import OrderedDict
from config import TAM_TLB

class TLBEntry:
    def __init__(self, vpn, pfn, pid):
        self.vpn = vpn  # Número da Página Virtual
        self.pfn = pfn  # Número do Frame Físico
        self.pid = pid  # ID do Processo
        self.valid = True

class TLB:
    def __init__(self, size=None):
        # Usa o tamanho do arquivo de configuração se não for especificado
        self.size = size if size is not None else TAM_TLB
        # Usando OrderedDict para implementar a política de substituição LRU
        # O parâmetro size determina quantas entradas a TLB pode armazenar
        self.entries = OrderedDict()  # Chave: (pid, vpn), Valor: TLBEntry
        self.hits = 0
        self.misses = 0

    def lookup(self, pid, vpn):
        """
        Procura um número de página virtual na TLB.
        Retorna o número do frame físico se encontrado, None caso contrário.
        """
        key = (pid, vpn)
        if key in self.entries:
            # Move a entrada para o final (mais recentemente usada)
            entry = self.entries.pop(key)
            self.entries[key] = entry
            self.hits += 1
            return entry.pfn
        self.misses += 1
        return None

    def insert(self, pid, vpn, pfn):
        """
        Insere uma nova tradução na TLB.
        Se a TLB estiver cheia, a entrada menos recentemente usada é removida.
        """
        key = (pid, vpn)
        # Se a entrada já existe, atualiza ela
        if key in self.entries:
            self.entries.pop(key)
        
        # Se a TLB estiver cheia, remove a entrada menos recentemente usada
        if len(self.entries) >= self.size:
            self.entries.popitem(last=False)  # Remove o primeiro item (mais antigo)
        
        # Adiciona a nova entrada
        self.entries[key] = TLBEntry(vpn, pfn, pid)

    def invalidate(self, pid=None):
        """
        Invalida entradas da TLB.
        Se pid for fornecido, invalida apenas as entradas daquele processo.
        Caso contrário, invalida todas as entradas.
        """
        if pid is None:
            self.entries.clear()
        else:
            # Remove todas as entradas do processo especificado
            keys_to_remove = [key for key in self.entries.keys() if key[0] == pid]
            for key in keys_to_remove:
                del self.entries[key]

    def get_stats(self):
        """
        Retorna estatísticas de hits e misses da TLB.
        """
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            'hits': self.hits,
            'misses': self.misses,
            'total': total,
            'hit_rate': hit_rate
        }