from enum import Enum


POLITICA_SUB = 0  # 0 para LRU, 1 para Relógio
TAM_MEM_PRINCIPAL = "128"
UNID_MEMP = "KB - KiloBytes"
TAM_PAGINA = "4"
UNID_PAG = "KB - KiloBytes"
NUM_LINHAS_TLB = "16"
TAM_MEM_SECUNDARIA = "512"
UNID_MEMS = "MB - MegaBytes"
TAM_QUADRO = TAM_PAGINA
UNID_QUAD = UNID_PAG
TAM_END_LOGICO = "16"
UNID_ENDLOG = "Bits"




MAPA_UNIDADES = {
    "KB - KiloBytes": 2 ** 10,
    "MB - MegaBytes": 2 ** 20
}
VALOR_PADRAO = 2**30

try:
    fator_mp = MAPA_UNIDADES.get(UNID_MEMP, VALOR_PADRAO)
    fator_pag = MAPA_UNIDADES.get(UNID_PAG, VALOR_PADRAO)
    
    TAMANHO_MEMORIA = int(TAM_MEM_PRINCIPAL) * fator_mp
    TAMANHO_PAGINA = int(TAM_PAGINA) * fator_pag
    TAMANHO_TLB = int(NUM_LINHAS_TLB)
except (ValueError, NameError) as e:
    print(f"Erro no config.py: {e}. Usando valores de fallback.")
    TAMANHO_MEMORIA = 128 * 1024
    TAMANHO_PAGINA = 4 * 1024
    TAMANHO_TLB = 16

class PoliticaSub(Enum):
    LRU = 0
    Relogio = 1

def ehPotenciaDeDois(n):
    if n <= 0: return False
    return (n & (n - 1)) == 0

def validarConfiguracoes():
    """
    Valida se as configurações estão em valores razoáveis.
    Retorna True se tudo estiver ok, False caso contrário.
    """
    # Usa a variável numérica TAMANHO_TLB para a verificação
    if TAMANHO_TLB <= 0:
        # A mensagem de erro refere-se à variável original do config
        print(f"ERRO: NUM_LINHAS_TLB ({NUM_LINHAS_TLB}) deve ser maior que zero.")
        return False
    
    if TAMANHO_PAGINA <= 0 or not ehPotenciaDeDois(TAMANHO_PAGINA):  # Potência de 2
        print(f"ERRO: TAM_PAGINA ({TAM_PAGINA}) deve ser maior que zero e uma potência de 2.")
        return False
    
    # Usa a variável numérica TAMANHO_MEMORIA para a verificação
    if TAMANHO_MEMORIA <= 0 or TAMANHO_MEMORIA < TAMANHO_PAGINA or not ehPotenciaDeDois(TAMANHO_MEMORIA):
        # A mensagem de erro refere-se à variável original do config
        print(f"ERRO: TAM_MEM_PRINCIPAL ({TAM_MEM_PRINCIPAL}) resulta em um tamanho de memória inválido. Deve ser maior que zero, maior que o tamanho da página e uma potência de 2.")
        return False
    
    return True

# Valida as configurações ao importar o módulo
if not validarConfiguracoes():
    raise ValueError("Configurações inválidas. Verifique o arquivo config.py")