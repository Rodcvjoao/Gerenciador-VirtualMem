from enum import Enum


POLITICA_SUB = 0  # 0 para LRU, 1 para Relógio
TAM_MEM_PRINCIPAL = "1024"
TAM_PAGINA = "8"
NUM_LINHAS_TLB = "8"
TAM_MEM_SECUNDARIA = "64"
TAM_QUADRO = "16"
TAM_END_LOGICO = "8"

# Vinda das informações da interface
TAM_MEM_PRINCIPAL = "1024"
TAM_MEM_SECUNDARIA = "64"
TAM_PAGINA = "8"
TAM_QUADRO = "16"
TAM_END_LOGICO = "8"
NUM_LINHAS_TLB = "8"


UNID_MEMP = "KB - KiloBytes"
UNID_MEMS = "KB - KiloBytes"
UNID_PAG = "KB - KiloBytes"
UNID_QUAD = "KB - KiloBytes"
UNID_ENDLOG = "KB - KiloBytes"


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
ARQ_TESTE = "lalalla"


# Define a política a ser usada na substituição de quadros na MP
# POLITICA_SUB = 0 -> LRU
# POLITICA_SUB = 1 -> RELÓGIO DE UM BIT
POLITICA_SUB = 0

class PoliticaSub(Enum):
    LRU = 0
    Relogio = 1

