from enum import Enum

# Configurações do sistema de memória virtual
# Estas configurações podem ser modificadas diretamente neste arquivo

# Vinda das informações da interface
TAM_MEM_PRINCIPAL = "1024"
TAM_MEM_SECUNDARIA = "64"
TAM_PAGINA_QUADRO = "128"
TAM_QUADRO = "2"
TAM_END_LOGICO = "8"
NUM_LINHAS_TLB = "64"

# Tratamento das strings para inteiros
TAMANHO_MEMORIA_P = int(TAM_MEM_PRINCIPAL)
TAMANHO_MEMORIA_S = int(TAM_MEM_SECUNDARIA)
TAMANHO_PAGINA_QUADRO = int(TAM_PAGINA_QUADRO)
TAMANHO_END_LOGICO = int(TAM_END_LOGICO)
NUMERO_LINHAS_TLB = int(NUM_LINHAS_TLB)

UNID_MEMP = "KB - KiloBytes"
UNID_MEMS = "KB - KiloBytes"
UNID_PAG_QUAD = "KB - KiloBytes"


lista_unidade = [UNID_MEMP, UNID_MEMS, UNID_PAG_QUAD]

# Tratamento das unidades em strings para inteiros
for i in range(len(lista_unidade)):
    if (lista_unidade[i] == "KB - KiloBytes"):
        lista_unidade[i] = 2 ** 10
    elif (lista_unidade[i] == "MB - MegaBytes"):
        lista_unidade[i] = 2 ** 20
    else:
        lista_unidade[i] = 2 ** 30


# Pegando o nome do arquivo teste
ARQ_TESTE = "aaaaaaaboa.py"


# Define a política a ser usada na substituição de quadros na MP
# POLITICA_SUB = 0 -> LRU
# POLITICA_SUB = 1 -> RELÓGIO DE UM BIT
POLITICA_SUB = 0

class PoliticaSub(Enum):
    LRU = 0
    Relogio = 1