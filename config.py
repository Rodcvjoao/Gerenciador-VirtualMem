# Configurações do sistema de memória virtual
# Estas configurações podem ser modificadas diretamente neste arquivo

# Tamanho da TLB (número de entradas)
TAMANHO_TLB = 16

# Tamanho da página em bytes (1MB)
TAMANHO_PAGINA = 2**20

# Tamanho total da memória física (1GB)
TAMANHO_MEMORIA = 2**30

# Função para verificar se um número é potência de 2
def ehPotenciaDeDois(n):
    if n <= 0:
        return False
    return (n & (n - 1)) == 0

# Função para validar as configurações
def validarConfiguracoes():
    """
    Valida se as configurações estão em valores razoáveis.
    Retorna True se tudo estiver ok, False caso contrário.
    """
    if TAMANHO_TLB <= 0:
        print("ERRO: TAMANHO_TLB deve ser maior que zero")
        return False
    
    if TAMANHO_PAGINA <= 0 or not ehPotenciaDeDois(TAMANHO_PAGINA):  #Potência de 2
        print("ERRO: TAMANHO_PAGINA deve ser maior que zero e potencia de 2.")
        return False
    
    if TAMANHO_MEMORIA <= 0 or TAMANHO_MEMORIA < TAMANHO_PAGINA:
        print("ERRO: TAMANHO_MEMORIA deve ser maior que zero e maior que TAMANHO_PAGINA")
        return False
    
    return True

# Valida as configurações ao importar o módulo
if not validarConfiguracoes():
    raise ValueError("Configurações inválidas. Verifique o arquivo config.py") 