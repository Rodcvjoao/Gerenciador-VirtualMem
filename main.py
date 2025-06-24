from memoriaPrincipal import MemoriaPrincipal
from tlb import TLB
from classesProcessos import Processo
from config import *

# ===================
# FUNÇÕES AUXILIARES 
# ===================

def tratar_acesso_memoria(processo, endereco_virtual, tlb, mp, tipo_acesso, processos_lista):
    """
    Orquestra a tradução de endereço, tratando acertos e falhas na TLB e na Tabela de Páginas.
    """
    print(f"P{processo.id}: Tentando acesso '{tipo_acesso}' ao endereço virtual {endereco_virtual}")
    processo.estado = "E"  # Executando

    # 1. Tenta traduzir o endereço usando o método do processo
    endereco_fisico, page_fault = processo.tabelaPaginas.traduzirEndereco(endereco_virtual, tlb)

    # 2. Trata o resultado
    if not page_fault:
        # Acesso bem-sucedido
        numero_pagina_virtual = endereco_virtual // TAMANHO_PAGINA
        entrada_tp = processo.tabelaPaginas.entradas[numero_pagina_virtual]
        numero_frame = entrada_tp.enderecoMemoriaPrincipal

        # Atualiza a referência para a política LRU
        quadro_acessado = mp.quadros[numero_frame]
        mp.referenciar_quadro_lru(quadro_acessado)

        # Atualiza a TLB (se foi um miss na TLB)
        tlb.inserir(processo.id, numero_pagina_virtual, numero_frame)
        
        print(f"P{processo.id}: Endereço encontrado na Memória Principal. Endereço Físico: {endereco_fisico}")

    else: # Ocorreu um Page Fault
        print(f"P{processo.id}: FALTA DE PÁGINA (Page Fault) para o endereço virtual {endereco_virtual}!")
        
        # 1. O processo é movido para o estado 'Bloqueado' (B)
        #    pois precisa esperar a operação de I/O do disco (carregar a página).
        processo.estado = "B"

        numero_pagina_necessaria = endereco_virtual // TAMANHO_PAGINA
        entrada_tp_necessaria = processo.tabelaPaginas.entradas[numero_pagina_necessaria]
        pagina_necessaria = entrada_tp_necessaria.pagina

        # A função agora retorna o quadro alocado e a página que foi substituída (se houver)
        quadro_alocado, pagina_substituida = mp.carregaPagina(processo, pagina_necessaria)

        # Se uma página foi de fato substituída, invalide sua antiga entrada na tabela de páginas
        if pagina_substituida is not None:
            # Encontra o processo dono da página substituída
            processo_dono = next((p for p in processos_lista if p.id == pagina_substituida.idProcesso), None)
            if processo_dono:
                entrada_antiga = processo_dono.tabelaPaginas.entradas[pagina_substituida.idPagina]
                entrada_antiga.bitPresenca = False
                entrada_antiga.enderecoMemoriaPrincipal = None
                print(f"Página {pagina_substituida.idPagina} do processo P{processo_dono.id} invalidada na Tabela de Páginas.")

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
            tratar_acesso_memoria(processo_atual, endereco_virtual, tlb, mp, tipoComando, processosLista)

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