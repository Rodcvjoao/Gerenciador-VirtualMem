from enum import Enum

# Configurações do sistema de memória virtual
# Estas configurações podem ser modificadas diretamente neste arquivo


# Vinda das informações da interface
TAM_MEM_PRINCIPAL = "8"
TAM_MEM_SECUNDARIA = "4"
TAM_PAGINA = "8"
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

UNID_MEMP = "KB"
UNID_MEMS = "KB"
UNID_PAG = "KB"
UNID_QUAD = "KB"
UNID_ENDLOG = "KB"


lista_unidade = [UNID_MEMP, UNID_MEMS, UNID_PAG, UNID_QUAD, UNID_ENDLOG]

# Tratamento das unidades em strings para inteiros
for i in range(len(lista_unidade)):
    if (lista_unidade[i] == "KB - KiloBytes"):
        lista_unidade[i] = 2 ** 10
    elif (lista_unidade[i] == "MB - MegaBytes"):
        lista_unidade[i] = 2 ** 20
    else:
        lista_unidade[i] = 2 ** 30


# Pegando o nome do arquivo teste
ARQ_TESTE = "aleluia.py"


# Define a política a ser usada na substituição de quadros na MP
# POLITICA_SUB = 0 -> LRU
# POLITICA_SUB = 1 -> RELÓGIO DE UM BIT
POLITICA_SUB = 0

class PoliticaSub(Enum):
    LRU = 0
    Relogio = 1

