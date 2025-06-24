from memoriaPrincipal import MemoriaPrincipal
from tlb import TLB
from classesProcessos import Processo
from config import *

# ===================
# FUNÇÕES AUXILIARES 
# ===================

def tratar_acesso_memoria(processo, endereco_virtual, tlb, mp, tipo_acesso):
    """
    Orquestra a tradução de endereço, tratando acertos e falhas na TLB e na Tabela de Páginas.
    """
    print(f"P{processo.id}: Tentando acesso '{tipo_acesso}' ao endereço virtual {endereco_virtual}")
    processo.estado = "E"  # Executando

    # 1. Tentar buscar na TLB primeiro
    numero_frame = tlb.buscar(processo.id, endereco_virtual // TAMANHO_PAGINA)
    
    if numero_frame is not None:
        # Acerto na TLB (TLB Hit)
        offset = endereco_virtual % TAMANHO_PAGINA
        endereco_fisico = numero_frame * TAMANHO_PAGINA + offset
        print(f"P{processo.id}: Acerto na TLB! Endereço Físico: {endereco_fisico}")
    else:
        # Falha na TLB (TLB Miss)
        print(f"P{processo.id}: Falha na TLB. Consultando Tabela de Páginas...")
        
        # 2. Consultar a Tabela de Páginas
        entrada_tp = processo.tabelaPaginas.entradas[endereco_virtual // TAMANHO_PAGINA]

        if not entrada_tp.bitPresenca:
            # Falta de Página (Page Fault)
            print(f"P{processo.id}: FALTA DE PÁGINA (Page Fault) para a página {endereco_virtual // TAMANHO_PAGINA}!")
            processo.estado = "B" # Bloqueia o processo enquanto trata a falta
            
            pagina_necessaria = entrada_tp.pagina
            
            # 3. Chamar a Memória Principal para carregar a página (e possivelmente substituir)
            quadro_alocado = mp.carregaPagina(processo, pagina_necessaria)
            
            # TODO: Atualizar a Entrada da Tabela de Páginas com as informações corretas
            # entrada_tp.bitPresenca = True
            # entrada_tp.enderecoMemoriaPrincipal = quadro_alocado.idQuadro
            
            print(f"P{processo.id}: Página {pagina_necessaria.idPagina} carregada no quadro {quadro_alocado.idQuadro}.")
            
            # 4. Agora que a página está na memória, insira na TLB
            tlb.inserir(processo.id, endereco_virtual // TAMANHO_PAGINA, quadro_alocado.idQuadro)
            
            # Processo volta para o estado de Pronto
            processo.estado = "P"

        else:
            # Página encontrada na Tabela de Páginas
            numero_frame = entrada_tp.enderecoMemoriaPrincipal
            offset = endereco_virtual % TAMANHO_PAGINA
            endereco_fisico = numero_frame * TAMANHO_PAGINA + offset
            print(f"P{processo.id}: Página encontrada na Tabela de Páginas. Endereço Físico: {endereco_fisico}")
            
            # 5. Inserir na TLB para futuros acessos
            tlb.inserir(processo.id, endereco_virtual // TAMANHO_PAGINA, numero_frame)

    # Se o acesso for de escrita, marcar a página como modificada
    if tipo_acesso == "W":
        print(f"P{processo.id}: Marcando página como modificada.")
        # TODO: Encontrar o objeto da página na memória e setar pagina.modificada = True
        # pagina_acessada = ...
        # pagina_acessada.modificada = True


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