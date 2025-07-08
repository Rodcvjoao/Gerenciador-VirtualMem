from enum import Enum
import math

class PoliticaSubstituicao(Enum):
    LRU = "LRU"
    RELOGIO = "RELOGIO"

# Vinda das informações da interface
TAM_MEM_PRINCIPAL = "32"
TAM_MEM_SECUNDARIA = "32"
TAM_PAGINA_QUADRO = "16"
TAM_END_LOGICO = "16"
NUM_LINHAS_TLB = "6"
POLITICA_SUBST = "LRU"

try:
    POLITICA_SUBST = PoliticaSubstituicao[POLITICA_SUBST.upper()]
except KeyError:
    print(f"Alerta: Política '{POLITICA_SUBST}' inválida. Usando RELOGIO como padrão.")
    POLITICA_SUBST = PoliticaSubstituicao.RELOGIO

# Tratamento das strings para inteiros
TAMANHO_MEMORIA_P = int(TAM_MEM_PRINCIPAL)
TAMANHO_MEMORIA_S = int(TAM_MEM_SECUNDARIA)
TAMANHO_PAGINA_QUADRO = int(TAM_PAGINA_QUADRO)
TAMANHO_END_LOGICO = int(TAM_END_LOGICO)
NUMERO_LINHAS_TLB = int(NUM_LINHAS_TLB)

# Unidades vindas da interface
UNID_MEMP = "KB - KiloBytes"
UNID_MEMS = "GB - GigaBytes"
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

UNID_MEMP, UNID_MEMS, UNID_PAG_QUAD = lista_unidade

TAMANHO_MEMORIA_P *= UNID_MEMP
TAMANHO_MEMORIA_S *= UNID_MEMS
TAMANHO_PAGINA_QUADRO *= UNID_PAG_QUAD

# Pegando o nome do arquivo teste
ARQ_TESTE = "caso_teste.txt"

MAPA_UNIDADES = {
    "B": 1,
    "KB": 2**10,
    "MB": 2**20,
    "GB": 2**30
}


BITS_OFFSET = (int(math.log2(TAMANHO_PAGINA_QUADRO)))
NUM_QUADROS_MEMORIA_PRINCIPAL = TAMANHO_MEMORIA_P // TAMANHO_PAGINA_QUADRO
