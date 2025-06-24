from enum import Enum

# Configurações do sistema de memória virtual
# Estas configurações podem ser modificadas diretamente neste arquivo


# Vinda das informações da interface
TAM_MEM_PRINCIPAL = "4"
TAM_MEM_SECUNDARIA = "4"
TAM_PAGINA = "2"
TAM_QUADRO = "2"
TAM_END_LOGICO = "2"
NUM_LINHAS_TLB = "2"

# Tratamento das strings para inteiros
TAMANHO_MEMORIA_P = int(TAM_MEM_PRINCIPAL)
TAMANHO_MEMORIA_S = int(TAM_MEM_SECUNDARIA)
TAMANHO_PAGINA = int(TAM_PAGINA)
TAMANHO_QUADRO = int(TAM_QUADRO)
TAMANHO_END_LOGICO = int(TAM_END_LOGICO)
NUMERO_LINHAS_TLB = int(NUM_LINHAS_TLB)


# Mapeamento de unidade para valor em bytes para centralizar a lógica
MAPA_UNIDADES = {
    "KB - KiloBytes": 2 ** 10,
    "MB - MegaBytes": 2 ** 20
}
# Valor padrão caso a unidade não seja KB ou MB (assumindo GB)
VALOR_PADRAO = 2 ** 30


# Pegando o nome do arquivo teste
ARQ_TESTE = "amem.py"


# Define a política a ser usada na substituição de quadros na MP
# POLITICA_SUB = 0 -> LRU
# POLITICA_SUB = 1 -> RELÓGIO DE UM BIT
POLITICA_SUB = 0

class PoliticaSub(Enum):
    LRU = 0
    Relogio = 1

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
    if NUMERO_LINHAS_TLB <= 0:
        print("ERRO: NUMERO_LINHAS_TLB deve ser maior que zero")
        return False
    
    if TAMANHO_PAGINA <= 0 or not ehPotenciaDeDois(TAMANHO_PAGINA):  #Potência de 2
        print("ERRO: TAMANHO_PAGINA deve ser maior que zero e potencia de 2.")
        return False
    
    if TAMANHO_MEMORIA <= 0 or TAMANHO_MEMORIA < TAMANHO_PAGINA or not ehPotenciaDeDois(TAMANHO_MEMORIA):
        print("ERRO: TAMANHO_MEMORIA deve ser maior que zero, maior que TAMANHO_PAGINA e potência de 2.")
        return False
    
    return True

# Valida as configurações ao importar o módulo
if not validarConfiguracoes():
    raise ValueError("Configurações inválidas. Verifique o arquivo config.py") 