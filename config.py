# Configurações do sistema de memória virtual
# Estas configurações podem ser modificadas diretamente neste arquivo


# Vinda das informações da interface
TAM_MEM_PRINCIPAL = "1024"
TAM_MEM_SECUNDARIA = "1024"
TAM_PAGINA = "4"
TAM_QUADRO = "4"
TAM_END_LOGICO = "4"
NUM_LINHAS_TLB = "4"


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
    if int(NUM_LINHAS_TLB) <= 0:
        print("ERRO: TAMANHO_TLB deve ser maior que zero")
        return False
    
    if int(TAM_PAGINA) <= 0 or not ehPotenciaDeDois(int(TAM_PAGINA)):  #Potência de 2
        print("ERRO: TAMANHO_PAGINA deve ser maior que zero e potencia de 2.")
        return False
    
    if int(TAM_MEM_PRINCIPAL) <= 0 or int(TAM_MEM_PRINCIPAL) < int(TAM_PAGINA):
        print("ERRO: TAMANHO_MEMORIA deve ser maior que zero e maior que TAMANHO_PAGINA")
        return False
    
    return True

# Valida as configurações ao importar o módulo
if not validarConfiguracoes():
    raise ValueError("Configurações inválidas. Verifique o arquivo config.py") 