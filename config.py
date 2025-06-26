from enum import Enum
import math

# =================================================================================
# ARQUIVO DE CONFIGURAÇÃO CENTRAL
# =================================================================================
# Modifique os valores das strings abaixo para configurar a simulação.
# As unidades podem ser "B" (Bytes), "KB" (KiloBytes), "MB" (MegaBytes), "GB" (GigaBytes).
# Os valores numéricos e as unidades são combinados para calcular o tamanho final em bytes.
# =================================================================================

# --- Configurações da Memória ---
TAMANHO_MEMORIA_PRINCIPAL_STR = "32 KB"
TAMANHO_MEMORIA_SECUNDARIA_STR = "1024 MB"
TAMANHO_PAGINA_QUADRO_STR = "16 KB"

# --- Configurações do Endereçamento e TLB ---
TAMANHO_ENDERECO_LOGICO_BITS = 80
NUMERO_LINHAS_TLB = 100

# --- Política de Substituição de Página ---
# Escolha a política a ser usada:
# - PoliticaSubstituicao.LRU
# - PoliticaSubstituicao.RELOGIO
POLITICA_ATUAL = "LRU"

# --- Arquivo de Teste ---
# Nome do arquivo de texto com a sequência de comandos para a simulação.
ARQUIVO_TESTE = "caso_teste.txt"

# =================================================================================
# (NÃO MODIFICAR ABAIXO DESTA LINHA)
# =================================================================================
# O código abaixo processa as strings de configuração e valida os valores.
# =================================================================================

class PoliticaSubstituicao(Enum):
    LRU = "LRU"
    RELOGIO = "RELOGIO"

# --- Dicionário para conversão de unidades para bytes ---
MAPA_UNIDADES = {
    "B": 1,
    "KB": 2**10,
    "MB": 2**20,
    "GB": 2**30
}

def _parse_tamanho(tamanho_str: str) -> int:
    """Converte uma string de tamanho (ex: "64 KB") para um valor inteiro em bytes."""
    try:
        partes = tamanho_str.strip().upper().split()
        valor = int(partes[0])
        unidade = partes[1]
        if unidade not in MAPA_UNIDADES:
            raise ValueError(f"Unidade '{unidade}' desconhecida. Use B, KB, MB ou GB.")
        return valor * MAPA_UNIDADES[unidade]
    except (ValueError, IndexError):
        raise ValueError(f"Formato de tamanho inválido: '{tamanho_str}'. Use um formato como '64 KB'.")

def _eh_potencia_de_dois(n):
    """Verifica se um número é uma potência de dois."""
    return (n > 0) and (n & (n - 1) == 0)

# --- Processamento e Validação das Configurações ---
try:
    # Conversão das strings para valores em bytes
    TAMANHO_MEMORIA_PRINCIPAL_BYTES = _parse_tamanho(TAMANHO_MEMORIA_PRINCIPAL_STR)
    TAMANHO_MEMORIA_SECUNDARIA_BYTES = _parse_tamanho(TAMANHO_MEMORIA_SECUNDARIA_STR)
    TAMANHO_PAGINA_QUADRO_BYTES = _parse_tamanho(TAMANHO_PAGINA_QUADRO_STR)

    # Validações de consistência e lógica
    if not _eh_potencia_de_dois(TAMANHO_MEMORIA_PRINCIPAL_BYTES):
        raise ValueError("O tamanho da memória principal deve ser uma potência de 2.")
    
    if not _eh_potencia_de_dois(TAMANHO_PAGINA_QUADRO_BYTES):
        raise ValueError("O tamanho da página/quadro deve ser uma potência de 2.")

    if TAMANHO_PAGINA_QUADRO_BYTES > TAMANHO_MEMORIA_PRINCIPAL_BYTES:
        raise ValueError("O tamanho da página não pode ser maior que o da memória principal.")

    if (TAMANHO_MEMORIA_PRINCIPAL_BYTES % TAMANHO_PAGINA_QUADRO_BYTES) != 0:
        raise ValueError("O tamanho da memória principal deve ser um múltiplo do tamanho da página/quadro.")

    # Calcula o número de bits para o offset (deslocamento)
    BITS_OFFSET = int(math.log2(TAMANHO_PAGINA_QUADRO_BYTES))
    if TAMANHO_ENDERECO_LOGICO_BITS <= BITS_OFFSET:
        raise ValueError("O tamanho do endereço lógico em bits deve ser maior que os bits de offset.")

    # Converte a política de string para Enum
    try:
        POLITICA_SUB = PoliticaSubstituicao(POLITICA_ATUAL.upper())
    except ValueError:
        raise ValueError(f"Política de substituição '{POLITICA_ATUAL}' inválida. Use 'LRU' ou 'RELOGIO'.")

    # Calcula o número total de quadros na memória principal
    NUM_QUADROS_MEMORIA_PRINCIPAL = TAMANHO_MEMORIA_PRINCIPAL_BYTES // TAMANHO_PAGINA_QUADRO_BYTES
    
    # Valida o número de linhas da TLB
    if NUMERO_LINHAS_TLB <= 0:
        raise ValueError("O número de linhas da TLB deve ser maior que zero.")

except ValueError as e:
    print(f"--- ERRO DE CONFIGURAÇÃO ---")
    print(f"Erro: {e}")
    print("Por favor, corrija o arquivo 'config.py' e tente novamente.")
    exit(1) # Termina a execução se a configuração for inválida

# Mensagem de sucesso se tudo estiver correto
print("✅ Configurações validadas com sucesso!")