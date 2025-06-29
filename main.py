import re
from memoriaPrincipal import MemoriaPrincipal
from tlb import TLB
from classesProcessos import Processo
from config import (
    ARQUIVO_TESTE, TAMANHO_MEMORIA_PRINCIPAL_STR, TAMANHO_PAGINA_QUADRO_STR,
    NUMERO_LINHAS_TLB, POLITICA_SUB, MAPA_UNIDADES, TAMANHO_PAGINA_QUADRO_BYTES
)

def tratar_acesso_memoria(processo: Processo, endereco_virtual: int, tlb: TLB, mp: MemoriaPrincipal, tipo_acesso: str, processos_lista: list[Processo]):
    """
    Função central para tratar um acesso à memória virtual por um processo.
    Coordena a tradução de endereços, tratamento de page faults e atualizações de estado.
    """
    print(f"\n[Acesso] P{processo.id}: Tentando acesso '{tipo_acesso}' ao endereço virtual {endereco_virtual}")
    processo.estado = "Executando"

    # Verifica se o endereço virtual está dentro dos limites do processo.
    if endereco_virtual >= processo.tamanho_bytes:
        print(f"!!! ERRO DE SEGMENTAÇÃO !!!: Endereço {endereco_virtual} (página {endereco_virtual // TAMANHO_PAGINA_QUADRO_BYTES}) "
              f"está fora do espaço de endereçamento do P{processo.id} (tamanho: {processo.tamanho_bytes} bytes).")
        processo.estado = "Finalizado (Erro)"
        return

    num_pagina_virtual = endereco_virtual // TAMANHO_PAGINA_QUADRO_BYTES
    
    # Tenta traduzir o endereço, consultando a TLB e depois a Tabela de Páginas.
    endereco_fisico, page_fault = processo.tabela_paginas.traduzir_endereco(endereco_virtual, tlb)

    if not page_fault:
        # ACESSO BEM-SUCEDIDO (Page Hit)
        print(f"P{processo.id}: Endereço encontrado na Memória Principal.")
        
        entrada_tp = processo.tabela_paginas.entradas[num_pagina_virtual]
        quadro_correspondente = mp.quadros[entrada_tp.endereco_quadro]
        
        # Atualiza bits para políticas de substituição.
        if quadro_correspondente.pagina:
            quadro_correspondente.pagina.referenciada = True
        quadro_correspondente.bit_utilizado = True # Para o algoritmo do Relógio.
        
        # Para LRU, move o quadro para o final da lista (mais recentemente usado).
        if quadro_correspondente in mp.quadros_refs_lru:
            mp.quadros_refs_lru.remove(quadro_correspondente)
        mp.quadros_refs_lru.append(quadro_correspondente)
        
        print(f"P{processo.id}: Endereço físico {endereco_fisico} acessado com sucesso.")
    else:
        # FALTA DE PÁGINA (Page Fault)
        print(f"P{processo.id}: FALTA DE PÁGINA para o endereço virtual {endereco_virtual}!")
        processo.estado = "Bloqueado"

        pagina_necessaria = processo.tabela_paginas.entradas[num_pagina_virtual].pagina
        quadro_alocado, pagina_substituida = mp.carrega_pagina(processo, pagina_necessaria)

        if pagina_substituida:
            # Encontra o processo dono da página que foi removida.
            processo_dono = next((p for p in processos_lista if p.id == pagina_substituida.id_processo), None)
            if processo_dono:
                entrada_antiga = processo_dono.tabela_paginas.entradas[pagina_substituida.id_pagina]
                entrada_antiga.bit_presenca = False
                entrada_antiga.endereco_quadro = -1
                tlb.invalidar_entrada(processo_dono.id, pagina_substituida.id_pagina)
                print(f"Tabela de Páginas de P{processo_dono.id} (página {pagina_substituida.id_pagina}) invalidada.")

        # Atualiza a tabela de páginas do processo atual com a nova informação.
        entrada_atual = processo.tabela_paginas.entradas[num_pagina_virtual]
        entrada_atual.bit_presenca = True
        entrada_atual.endereco_quadro = quadro_alocado.id_quadro
        print(f"P{processo.id}: Página {pagina_necessaria.id_pagina} carregada no quadro {quadro_alocado.id_quadro}.")

        # Como a página foi trazida para a memória, sua tradução é inserida na TLB.
        tlb.inserir(processo.id, num_pagina_virtual, quadro_alocado.id_quadro)
        
        processo.estado = "Pronto"

    if tipo_acesso == "W":
        # Marca a página como modificada (dirty bit) em caso de escrita.
        entrada_tp = processo.tabela_paginas.entradas[num_pagina_virtual]
        if entrada_tp.endereco_quadro is not None:
            quadro_correspondente = mp.quadros[entrada_tp.endereco_quadro]
            if quadro_correspondente.pagina:
                quadro_correspondente.pagina.modificada = True
            entrada_tp.bit_modificacao = True
            print(f"P{processo.id}: Página {num_pagina_virtual} marcada como modificada (M=1).")

    if processo.estado == "Executando":
        processo.estado = "Pronto"

def print_estado_sistema(mp: MemoriaPrincipal, tlb: TLB, processos: list[Processo], ciclo: int):
    """Imprime um resumo completo do estado atual do sistema."""
    print("\n" + "="*60)
    print(f"FIM DO CICLO {ciclo}: ESTADO DO SISTEMA")
    print("="*60)
    
    # --- Estado dos Processos ---
    print("\n--- 1. Fila de Processos ---")
    prontos = [f"P{p.id}" for p in processos if p.estado == 'Pronto']
    executando = [f"P{p.id}" for p in processos if p.estado == 'Executando']
    bloqueados = [f"P{p.id}" for p in processos if p.estado == 'Bloqueado']
    print(f"  - Prontos: {prontos if prontos else 'Nenhum'}")
    print(f"  - Executando: {executando if executando else 'Nenhum'}")
    print(f"  - Bloqueados: {bloqueados if bloqueados else 'Nenhum'}")

    # --- Estado da Memória Principal ---
    print("\n--- 2. Memória Principal (Quadros) ---")
    for quadro in mp.quadros:
        if quadro.ocupado and quadro.pagina:
            pagina = quadro.pagina
            print(f"  - Quadro {quadro.id_quadro:02d}: Ocupado por P{pagina.id_processo} (Página {pagina.id_pagina}) "
                  f"[M={int(pagina.modificada)}, U={int(quadro.bit_utilizado)}]")
        else:
            print(f"  - Quadro {quadro.id_quadro:02d}: Livre")
    
    # --- Estado da TLB ---
    tlb.print_estado()
    print("="*60 + "\n")

def executar_simulacao(caminho_arquivo: str): 
    """Função principal que carrega o arquivo de teste e executa a simulação ciclo a ciclo."""
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f: 
            comandos = [tuple(line.strip().split()) for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Erro: Arquivo de teste '{caminho_arquivo}' não encontrado.") 
        return
    
    mp = MemoriaPrincipal()
    tlb = TLB()
    processos_lista = []
    ciclo = 0

    print("="*50)
    print("INICIANDO SIMULADOR DE MEMÓRIA VIRTUAL")
    print("="*50)
    print(f"  - Arquivo de Comandos: {caminho_arquivo}")
    print(f"  - Memória Principal: {TAMANHO_MEMORIA_PRINCIPAL_STR}")
    print(f"  - Tamanho da Página/Quadro: {TAMANHO_PAGINA_QUADRO_STR}")
    print(f"  - Entradas na TLB: {NUMERO_LINHAS_TLB}")
    print(f"  - Política de Substituição: {POLITICA_SUB.value}")
    print("="*50 + "\n")

    for comando in comandos:
        ciclo += 1
        print(f"--- CICLO {ciclo}: Processando Comando: {' '.join(comando)} ---")

        id_processo = int(comando[0][1:])
        tipo_comando = comando[1].upper()
        
        processo_atual = next((p for p in processos_lista if p.id == id_processo), None)

        if not processo_atual and tipo_comando != "C":
            print(f"Erro: Tentativa de operar no processo P{id_processo}, que não existe.")
            continue

        try:
            if tipo_comando == "C":
                tamanho_str = f"{comando[2]} {comando[3]}"
                # Converte a string (ex: "128 KB") para bytes
                tamanho_bytes = int(comando[2]) * MAPA_UNIDADES[comando[3].upper()]
                
                novo_processo = Processo(id_processo, tamanho_bytes)
                processos_lista.append(novo_processo)
                novo_processo.estado = "Pronto"

            elif processo_atual: # Garante que o processo existe para os outros comandos
                if tipo_comando in ["R", "P", "W"]:
                    # Extrai o endereço de formatos como "A(1234)" ou "1234"
                    match = re.search(r'\((\d+)\)', comando[2])
                    addr = int(match.group(1)) if match else int(comando[2])
                    tratar_acesso_memoria(processo_atual, addr, tlb, mp, tipo_comando, processos_lista)

                elif tipo_comando == "I":
                    print(f"P{id_processo}: Instrução de I/O. Processo movido para Bloqueado.")
                    processo_atual.estado = "Bloqueado"

                elif tipo_comando == "T":
                    print(f"P{id_processo}: Finalizando processo.")
                    processo_atual.estado = "Finalizado"
                    tlb.invalidar_processo(id_processo)
                    # Remove o processo da lista de ativos
                    processos_lista = [p for p in processos_lista if p.id != id_processo]
        
        except (ValueError, KeyError, IndexError) as e:
            print(f"!!! ERRO no comando '{' '.join(comando)}': {e}. Pulando comando.")
            continue
            
        print_estado_sistema(mp, tlb, processos_lista, ciclo)

    print("\n--- SIMULAÇÃO FINALIZADA ---")

# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    executar_simulacao(ARQUIVO_TESTE)