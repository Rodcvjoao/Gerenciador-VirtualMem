import re
from memoriaPrincipal import MemoriaPrincipal
from tlb import TLB
from classesProcessos import Processo
from config import *

# ... (FUNÇÕES AUXILIARES) ...
def tratar_acesso_memoria(processo, endereco_virtual, tlb, mp, tipo_acesso, processos_lista):
    """
    Trata um acesso à memória virtual, lidando com tradução de endereços,
    page faults, e atualizações de bits de controle.
    
    Args:
        processo: Processo que está fazendo o acesso
        endereco_virtual: Endereço virtual a ser acessado
        tlb: Translation Lookaside Buffer
        mp: Memória Principal
        tipo_acesso: Tipo de acesso ('R' = Read, 'W' = Write, 'P' = Program)
        processos_lista: Lista de todos os processos ativos
    """
    
    print(f"\n[Acesso] P{processo.id}: Tentando acesso '{tipo_acesso}' ao endereço virtual {endereco_virtual}")
    processo.estado = "E"  # Processo em execução

    # Calcula o número da página virtual
    numero_pagina_virtual = endereco_virtual // TAMANHO_PAGINA_QUADRO
    
    # Verifica se o endereço está dentro do espaço de endereçamento do processo
    if numero_pagina_virtual >= processo.quantidadePaginas:
        print(f"!!! ERRO DE SEGMENTAÇÃO !!!: Endereço {endereco_virtual} está fora do espaço de endereçamento do P{processo.id}.")
        processo.estado = "F"  # Processo finalizado por erro
        return

    # Tenta traduzir o endereço virtual para físico
    endereco_fisico, page_fault = processo.tabelaPaginas.traduzirEndereco(endereco_virtual, tlb)

    if not page_fault:
        # ACESSO BEM-SUCEDIDO - Página está na memória principal
        print(f"P{processo.id}: Endereço encontrado na Memória Principal.")
        
        # Atualizar bits de referência e controle
        entrada_tp = processo.tabelaPaginas.entradas[numero_pagina_virtual]
        quadro_correspondente = mp.quadros[entrada_tp.enderecoMemoriaPrincipal]
        
        # Marca a página como referenciada (importante para algoritmos de substituição)
        quadro_correspondente.pagina.referenciada = True
        quadro_correspondente.bitUtilizado = True
        
        # Atualizar lista LRU - move para o final (mais recentemente usado)
        if quadro_correspondente in mp.quadrosRefsLRU:
            mp.quadrosRefsLRU.remove(quadro_correspondente)
        mp.quadrosRefsLRU.append(quadro_correspondente)
        
        print(f"P{processo.id}: Endereço físico {endereco_fisico} acessado com sucesso.")
        
    else:
        # PAGE FAULT - Página não está na memória principal
        print(f"P{processo.id}: FALTA DE PÁGINA (Page Fault) para o endereço virtual {endereco_virtual}!")
        processo.estado = "B"  # Processo bloqueado aguardando I/O

        # Busca a página que precisa ser carregada
        pagina_necessaria = processo.tabelaPaginas.entradas[numero_pagina_virtual].pagina
        
        # Carrega a página na memória principal
        quadro_alocado, pagina_substituida = mp.carregaPagina(processo, pagina_necessaria)

        # Se uma página foi substituída, precisa invalidar suas referências
        if pagina_substituida:
            # Encontra o processo dono da página substituída
            processo_dono = next((p for p in processos_lista if p.id == pagina_substituida.idProcesso), None)
            
            if processo_dono:
                # Invalida a entrada na tabela de páginas do processo dono
                entrada_antiga = processo_dono.tabelaPaginas.entradas[pagina_substituida.idPagina]
                entrada_antiga.bitPresenca = False
                entrada_antiga.enderecoMemoriaPrincipal = None
                
                # Invalida a entrada correspondente na TLB
                tlb.invalidar_entrada(processo_dono.id, pagina_substituida.idPagina)
                
                print(f"Página {pagina_substituida.idPagina} do processo P{processo_dono.id} invalidada.")

        # Atualiza a tabela de páginas do processo atual
        entrada_atual = processo.tabelaPaginas.entradas[numero_pagina_virtual]
        entrada_atual.bitPresenca = True
        entrada_atual.enderecoMemoriaPrincipal = quadro_alocado.idQuadro
        
        print(f"P{processo.id}: Página {pagina_necessaria.idPagina} carregada no quadro {quadro_alocado.idQuadro}.")

        # Insere a nova tradução na TLB
        tlb.inserir(processo.id, numero_pagina_virtual, quadro_alocado.idQuadro)
        
        # Processo volta ao estado pronto
        processo.estado = "P"

    # TRATAMENTO ESPECÍFICO PARA OPERAÇÕES DE ESCRITA
    if tipo_acesso == "W":
        # Marca a página como modificada (dirty bit)
        entrada_tp = processo.tabelaPaginas.entradas[numero_pagina_virtual]
        quadro_correspondente = mp.quadros[entrada_tp.enderecoMemoriaPrincipal]
        
        # Atualiza os bits de modificação
        quadro_correspondente.pagina.modificada = True
        entrada_tp.bitModificacao = True
        
        print(f"P{processo.id}: Página {numero_pagina_virtual} marcada como modificada (M=1).")

    # ATUALIZAÇÃO FINAL DO ESTADO DO PROCESSO
    if processo.estado == "E":
        processo.estado = "P"  # Volta para pronto após completar o acesso

        
def print_estado_sistema(mp, tlb, processos):
    print("\n" + "="*50)
    print("ESTADO ATUAL DO SISTEMA")
    print("="*50)
    tlb.print_estado()
    print("\n--- Estado dos Processos ---")
    for p in processos:
        print(f"  P{p.id} - Estado: {p.estado}")
    print("="*50 + "\n")


# =================================================================================
# BLOCO PRINCIPAL (MAIN)
# =================================================================================

def executar_simulacao(caminho_arquivo_teste): 
    try:
        with open(caminho_arquivo_teste, "r", encoding="utf-8") as f: 
            seqComandos = [tuple(line.strip().split()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Erro: Arquivo de teste '{caminho_arquivo_teste}' não encontrado.") 
        return
    
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo de teste: {e}")
        return

    mp = MemoriaPrincipal()
    tlb = TLB()
    processosLista = []
    ciclo = 0

    print("="*50)
    print("CONFIGURAÇÕES DA SIMULAÇÃO CARREGADAS")
    print("="*50)
    print(f"  - Arquivo de Teste: {caminho_arquivo_teste}")
    print(f"  - Tamanho da Memória Principal: {TAMANHO_MEMORIA_P} {UNID_MEMP}")
    print(f"  - Tamanho da Página/Quadro: {TAMANHO_PAGINA_QUADRO} {UNID_PAG_QUAD}")
    print(f"  - Número de Linhas da TLB: {NUMERO_LINHAS_TLB}")
    politica = "LRU (Least Recently Used)" if POLITICA_SUB == 0 else "Relógio"
    print(f"  - Política de Substituição: {politica}")
    print("="*50 + "\n")

    print("--- INICIANDO SIMULAÇÃO ---")
    for comando in seqComandos:
        ciclo += 1
        print(f"--- Ciclo {ciclo}: Executando Comando: {' '.join(comando)} ---")

        idProcesso = int(comando[0][1:])
        tipoComando = comando[1].upper()
        
        processo_atual = next((p for p in processosLista if p.id == idProcesso), None)

        if not processo_atual and tipoComando != "C":
            print(f"Erro: Tentando operar no processo P{idProcesso} que não existe.")
            continue

        if tipoComando == "C":
            tamanho, unidade = int(comando[2]), comando[3]
            if unidade == "KB": tamProcesso = tamanho * 1024
            elif unidade == "MB": tamProcesso = tamanho * 1024 * 1024
            else: tamProcesso = tamanho * 1024 * 1024 * 1024
            
            novo_processo = Processo(idProcesso, tamProcesso)
            processosLista.append(novo_processo)
            print(f"P{idProcesso}: Processo criado com tamanho {tamProcesso} bytes.")
            novo_processo.estado = "P"

        elif tipoComando in ["R", "P", "W"]:
            match = re.search(r'\((\d+)\)', comando[2])
            if match:
                endereco_virtual = int(match.group(1))
            else:
                try:
                    endereco_virtual = int(comando[2])
                except ValueError:
                    print(f"Erro: Formato de endereço inválido no comando: {' '.join(comando)}")
                    continue
            
            tratar_acesso_memoria(processo_atual, endereco_virtual, tlb, mp, tipoComando, processosLista)

        elif tipoComando == "I":
            print(f"P{idProcesso}: Instrução de I/O. Processo movido para Bloqueado.")
            processo_atual.estado = "B"

        elif tipoComando == "T":
            print(f"P{idProcesso}: Processo finalizado.")
            processo_atual.estado = "F"
            tlb.invalidar_processo(idProcesso)
            processosLista.remove(processo_atual)
            
        print_estado_sistema(mp, tlb, processosLista)

    print("\n--- Simulação Finalizada ---")