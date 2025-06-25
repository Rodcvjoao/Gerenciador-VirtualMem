from enum import Enum


POLITICA_SUB = 0  # 0 para LRU, 1 para Relógio
TAM_MEM_PRINCIPAL = "128"
TAM_PAGINA = "4"
NUM_LINHAS_TLB = "16"
TAM_MEM_SECUNDARIA = "512"
TAM_QUADRO = TAM_PAGINA
TAM_END_LOGICO = "16"

# Vinda das informações da interface
TAM_MEM_PRINCIPAL = "8"
TAM_MEM_SECUNDARIA = "4"
TAM_PAGINA = "8"
TAM_QUADRO = "2"
TAM_END_LOGICO = "2"
NUM_LINHAS_TLB = "2"


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

