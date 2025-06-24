# Configurações do sistema de memória virtual
# Estas configurações podem ser modificadas diretamente neste arquivo


# Vinda das informações da interface
TAM_MEM_PRINCIPAL = "1"
TAM_MEM_SECUNDARIA = "1"
TAM_PAGINA = "1"
TAM_QUADRO = "11"
TAM_END_LOGICO = "1"
NUM_LINHAS_TLB = "1"

# Tratamento das strings para inteiros
TAMANHO_MEMORIA_P = int(TAM_MEM_PRINCIPAL)
TAMANHO_MEMORIA_S = int(TAM_MEM_SECUNDARIA)
TAMANHO_PAGINA = int(TAM_PAGINA)
TAMANHO_QUADRO = int(TAM_QUADRO)
TAMANHO_END_LOGICO = int(TAM_END_LOGICO)
NUMERO_LINHAS_TLB = int(NUM_LINHAS_TLB)


#Vinda da informação das unidades da interface - KB (2 ** 10), MB ( 2 ** 20 ) ou GB ( 2 ** 30 )
UNID_MEMP = "KB - KiloBytes"
UNID_MEMS = "MB - MegaBytes"
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
ARQ_TESTE = "aaaa.py"


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
        print("ERRO: TAMANHO_TLB deve ser maior que zero")
        return False
    
    if TAMANHO_PAGINA <= 0 or not ehPotenciaDeDois(TAMANHO_PAGINA):  #Potência de 2
        print("ERRO: TAMANHO_PAGINA deve ser maior que zero e potencia de 2.")
        return False
    
    if TAMANHO_MEMORIA_P <= 0 or TAMANHO_MEMORIA_P < TAMANHO_PAGINA:
        print("ERRO: TAMANHO_MEMORIA deve ser maior que zero e maior que TAMANHO_PAGINA")
        return False
    
    return True

# Valida as configurações ao importar o módulo
if not validarConfiguracoes():
    raise ValueError("Configurações inválidas. Verifique o arquivo config.py") 