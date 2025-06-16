# Configurações do sistema de memória virtual
# Estas configurações podem ser modificadas diretamente neste arquivo

# Tamanho da TLB (número de entradas)
TAM_TLB = 16

# Tamanho da página em bytes (1MB)
TAM_PAGINA = 2**20

# Tamanho total da memória física (1GB)
TAM_MEMORIA = 2**30

# Função para validar as configurações
def validar_config():
    """
    Valida se as configurações estão em valores razoáveis.
    Retorna True se tudo estiver ok, False caso contrário.
    """
    if TAM_TLB <= 0:
        print("ERRO: TAM_TLB deve ser maior que zero")
        return False
    
    if TAM_PAGINA <= 0 or TAM_PAGINA % 4096 != 0:  # Múltiplo de 4KB
        print("ERRO: TAM_PAGINA deve ser maior que zero e múltiplo de 4KB")
        return False
    
    if TAM_MEMORIA <= 0 or TAM_MEMORIA < TAM_PAGINA:
        print("ERRO: TAM_MEMORIA deve ser maior que zero e maior que TAM_PAGINA")
        return False
    
    return True

# Valida as configurações ao importar o módulo
if not validar_config():
    raise ValueError("Configurações inválidas. Verifique o arquivo config.py") 