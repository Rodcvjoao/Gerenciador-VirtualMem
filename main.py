from memoriaPrincipal import MemoriaPrincipal
from tlb import TLB
from classesProcessos import Processo
from config import *

# ===================
# FUNÇÕES AUXILIARES 
# ===================


#alteração para uso melhor das classes - pietro
def tratar_acesso_memoria(processo, endereco_virtual, tlb, mp, tipo_acesso):
    """
    Orquestra a tradução de endereço, tratando acertos e falhas na TLB e na Tabela de Páginas.
    """
    print(f"P{processo.id}: Tentando acesso '{tipo_acesso}' ao endereço virtual {endereco_virtual}")
    processo.estado = "E"  # Executando

    # 1. Tenta traduzir o endereço usando o método do processo
    endereco_fisico, page_fault = processo.tabelaPaginas.traduzirEndereco(endereco_virtual, tlb)

    # 2. Trata o resultado
    if not page_fault:
        # Acesso bem-sucedido (pode ter sido TLB hit ou miss, mas a página está na memória)
        numero_pagina_virtual = endereco_virtual // TAMANHO_PAGINA
        
        # Se foi TLB miss (caso contrário a função teria retornado antes), a TLB é atualizada
        entrada_tp = processo.tabelaPaginas.entradas[numero_pagina_virtual]
        tlb.inserir(processo.id, numero_pagina_virtual, entrada_tp.enderecoMemoriaPrincipal)
        
        print(f"P{processo.id}: Endereço encontrado na Memória Principal. Endereço Físico: {endereco_fisico}")

    else: # Ocorreu um Page Fault
        print(f"P{processo.id}: FALTA DE PÁGINA (Page Fault) para o endereço virtual {endereco_virtual}!")
        processo.estado = "B" # Bloqueia o processo enquanto trata a falta

        numero_pagina_necessaria = endereco_virtual // TAMANHO_PAGINA
        entrada_tp_necessaria = processo.tabelaPaginas.entradas[numero_pagina_necessaria]
        pagina_necessaria = entrada_tp_necessaria.pagina

        # 3. Informa a Memória Principal para carregar a página
        # A MP irá encontrar um quadro livre ou substituir uma página e retornará o quadro usado.
        quadro_alocado = mp.carregaPagina(processo, pagina_necessaria)

        # Antes de atualizar a nova entrada, invalida a entrada da página antiga (se houve substituição)
        if quadro_alocado.pagina.idPagina != pagina_necessaria.idPagina: # Checa se a página no quadro é a que acabou de sair
             pagina_antiga = quadro_alocado.pagina 
             # IMPORTANTE: Esta lógica assume que a pagina antiga ainda está no quadro.
             # O ideal é a função de substituição retornar a pagina antiga também.
             # Para simplificar, vamos buscar o processo dono da pagina antiga e invalidar.
             # (Esta parte pode ser melhorada dependendo da complexidade desejada)
             pass # Lógica de invalidação da página antiga aqui...


        # 4. Atualiza a Tabela de Páginas do processo com o quadro alocado
        entrada_tp_necessaria.bitPresenca = True
        entrada_tp_necessaria.enderecoMemoriaPrincipal = quadro_alocado.idQuadro
        print(f"P{processo.id}: Página {pagina_necessaria.idPagina} carregada no quadro {quadro_alocado.idQuadro}.")

        # 5. Atualiza a TLB com a nova tradução
        tlb.inserir(processo.id, numero_pagina_necessaria, quadro_alocado.idQuadro)

        # Recalcula o endereço físico agora que a página está na memória
        offset = endereco_virtual % TAMANHO_PAGINA
        endereco_fisico = quadro_alocado.idQuadro * TAMANHO_PAGINA + offset
        print(f"P{processo.id}: Acesso ao endereço físico {endereco_fisico} pode prosseguir.")
        
        # Processo volta para o estado de Pronto
        processo.estado = "P"

    # Se o acesso for de escrita, marcar a página como modificada (Bit M = 1)
    if tipo_acesso == "W":
        numero_pagina_virtual = endereco_virtual // TAMANHO_PAGINA
        entrada_tp = processo.tabelaPaginas.entradas[numero_pagina_virtual]
        
        # Encontra o quadro correspondente na memória principal para setar o bit 'modificada'
        quadro_correspondente = mp.quadros[entrada_tp.enderecoMemoriaPrincipal]
        quadro_correspondente.pagina.modificada = True
        entrada_tp.bitModificacao = True # Também pode ser útil ter o bit na TP
        print(f"P{processo.id}: Página {numero_pagina_virtual} marcada como modificada (M=1).")

#fim da mudança 2

def print_estado_sistema(mp, tlb, processos):
    """
    Imprime o estado atual de todos os componentes do sistema para depuração.
    """
    print("\n" + "="*40)
    print("ESTADO ATUAL DO SISTEMA")
    print("="*40)
    
    # TODO: Implementar um método print_estado() na classe MemoriaPrincipal
    # mp.print_estado()
    

    tlb.print_estado()
    
    print("\n--- Estado dos Processos e Tabelas de Páginas ---")
    for p in processos:
        print(f"  P{p.id} - Estado: {p.estado}")
        # TODO: Implementar um método print_estado() na classe TabelaPaginas
        # p.tabelaPaginas.print_estado()

    print("="*40 + "\n")


# =================================================================================
# BLOCO PRINCIPAL (MAIN)
# =================================================================================

# Ler arquivo de comandos
try:
    with open("caso_de_teste.txt", "r", encoding="utf-8") as f:
        seqComandos = f.read().strip().split("\n")
        seqComandos = [tuple(c.split(" ")) for c in seqComandos]
except FileNotFoundError:
    print("Erro: Arquivo 'caso_de_teste.txt' não encontrado.")
    exit()

# Inicializar componentes do sistema
mp = MemoriaPrincipal()
tlb = TLB()
processosLista = []
ciclo = 0

# Loop principal da simulação
for comando in seqComandos:
    ciclo += 1
    print(f"--- Ciclo {ciclo}: Executando Comando: {' '.join(comando)} ---")

    idProcesso = int(comando[0][1:])
    tipoComando = comando[1]
    
    processo_atual = next((p for p in processosLista if p.id == idProcesso), None)

    match tipoComando:
        case "C":
            if processo_atual:
                print(f"Erro: Processo P{idProcesso} já existe.")
                continue

            tamanho, unidade = comando[2].split()
            tamanho = int(tamanho)
            
            # Converter tamanho para bytes com base na unidade
            if unidade == "KB":
                tamProcesso = tamanho * 1024
            elif unidade == "MB":
                tamProcesso = tamanho * 1024 * 1024
            elif unidade == "GB":
                tamProcesso = tamanho * 1024 * 1024 * 1024
            else:
                print(f"Erro: Unidade '{unidade}' inválida para tamanho do processo.")
                continue
            
            novo_processo = Processo(idProcesso, tamProcesso)
            processosLista.append(novo_processo)
            print(f"P{idProcesso}: Processo criado com tamanho {tamProcesso} bytes.")
            
            # Alocar páginas iniciais na memória
            mp.carregaProcesso(novo_processo)
            novo_processo.estado = "P" # Pronto

        case "R" | "P" | "W":
            if not processo_atual:
                print(f"Erro: Tentando acessar processo P{idProcesso} que não existe.")
                continue
            
            endereco_virtual = int(comando[2])
            tratar_acesso_memoria(processo_atual, endereco_virtual, tlb, mp, tipoComando)

        case "I":
            if not processo_atual:
                print(f"Erro: Tentando I/O no processo P{idProcesso} que não existe.")
                continue
            
            print(f"P{idProcesso}: Instrução de I/O. Processo movido para Bloqueado.")
            processo_atual.estado = "B"

        case "T":
            if not processo_atual:
                print(f"Erro: Tentando terminar processo P{idProcesso} que não existe.")
                continue
            
            print(f"P{idProcesso}: Processo finalizado. Liberando recursos...")
            processo_atual.estado = "F"
            # TODO: Implementar a lógica de liberação de quadros na MemoriaPrincipal
            # mp.libera_processo(processo_atual)
            
            
            tlb.invalidar()
            
    # Imprimir o estado do sistema ao final de cada ciclo
    print_estado_sistema(mp, tlb, processosLista)

print("--- Simulação Finalizada ---")