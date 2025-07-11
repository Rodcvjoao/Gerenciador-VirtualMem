# Gerenciador de Memória Virtual
# Trabalho de Sistemas Operacionais, specs:

## Objetivo
O objetivo deste trabalho é o de projetar e implementar um gerenciamento de memória virtual com paginação, através da simulação de execução de processos submetidos em um sistema computacional.

## Memória Virtual
Para gerenciar a memória, o gerenciador de memória (GM) implementa o esquema de paginação. Para tal, o GM mantém uma tabela de páginas *TP(Pi)* para cada processo *Pi* submetido. Cada entrada desta tabela deve pelo menos conter:
- o bit *P* de presença da referida página na memória principal (MP)
- o bit *M* de modificação da referida página
- número do quadro em MP, quando a referida página está em memória.

Páginas da imagem devem ser carregadas para quadros da MP quando necessário. Quando o processador requisitar acesso a um **endereço virtual/relativo**, um simulador do hardware que mapeia este endereço para o endereço real deve realizar o mapeamento, resultando no acesso ao **endereço real** caso a página esteja em memória, ou em caso de falta de página em MP, realizar os passos necessários para trazer a página para a MP (alocar um quadro que esteja disponível). Caso não haja disponibilidade, executar a **política de substituição de páginas**.

## Política de substituição de páginas
O gerenciador de memória deve utilizar um algoritmo de substituição de páginas, para alocar um quadro a uma página não residente em memória no caso em que todos os quadros da MP já estiverem alocados, e a falta de página ocorre ao executar um determinado processo. Algoritmos de substituição a serem implementados são:
- **LRU**
- **Relógio com um bit (bit u)**

O escopo de substituição é **global**, para ambas as políticas.

Inicialmente, o GM deve alocar devidamente um (ou mais) quadro(s) para o processo, quando este for criado para que ele se torne pronto (além obviamente criar as estruturas de dados necessárias). Caso não tenha memória disponível, o algoritmo de substituição deve prover qual quadro deve ser utilizado. Atenção, se o quadro escolhido armazenar uma página (a que será substituída) que foi modificada, a gravação desta deve ser realizada antes da carga da nova página a ser trazida para memória.

## TLB - Translation Lookaside Buffer
Para agilizar o acesso à Tabela de Páginas de um processo Pi em execução, a TLB é aqui implementada, com cache associativo. Especifique uma TLB com os campos necessários para o funcionamento correto.

## Configuração do sistema
Seu sistema GM deve conter as seguintes opções de configuração de mecanismos associados à memória virtual:
- Tamanho total da Memória física (que deve ser múltiplo de tamanho do quadro) e Memória Secundária
- Tamanho da página de um processo e quadro de memória;
- Tamanho em bits do endereço lógico.
- Número de linhas da TLB e seus campos necessários.

## Importante
Especificar as estruturas de dados necessárias para implementar cada política de substituição e escopo. Uma saída (interface amigável) deve mostrar:
- o que está acontecendo tanto na memória principal, quanto na secundária;
- a tabela de páginas associada a cada processo em execução;
- as ocorrências de falta de página;
- estado dos processos (e filas associadas).
- a TLB

## Simulando a execução de processos
A simulação deve ser realizada de acordo com a entrada de uma série de comandos que simulam o acesso à memória, criação, terminação e execução de instruções de um processo e instruções de entrada ou saída.

Seu simulador deve ler de um arquivo as informações sobre a "vida" dos processos, contendo para cada processo, o tamanho de sua imagem e uma sequência de operações de acesso à memória principal que o respectivo processo realiza.

## A entrada de seu simulador
Como entrada do simulador, representando a execução de um programa, uma sequência de situações pode ocorrer. Como sabemos, processos podem ter instruções executadas diretamente pela CPU ou pedidos de E/S. Sabemos ainda que para buscar tais instruções ou dados, pedidos de leitura devem ser executados. Para executar uma instrução, leitura ou gravação em memória principal podem ser realizadas.

Assim, flags são definidos para representar o que está acontecendo naquele momento em relação ao processo. Os seguintes flags serão utilizados:
- **Criação de processo (C):** Para cada processo, o arquivo deve informar o seu tamanho em bytes.
- **Acesso a endereço (R):** Acesso a endereço de memória para leitura (busca de instrução ou dado).
- **Acesso a endereço (W):** Acesso a endereço de memória para gravação (gravação de um dado).
- **Instrução de CPU (P):** Simula o processamento de uma instrução que não acessa memória.
- **Instrução de E/S (I):** Simula a execução de uma instrução de E/S, o que acarreta no bloqueio do processo.
- **Término de processo (T):** Simula o término de um processo.

**Formato do arquivo de entrada:**
O arquivo de entrada deve conter uma sequência de linhas, cada uma representando um comando para a simulação, no seguinte formato:
`[id do processo] [flag] [informação adicional]`

Exemplo:
`P1 C 1024` (Processo P1 criado com 1024 bytes)
`P1 R 200` (Processo P1 acessa o endereço 200 para leitura)
`P2 I` (Processo P2 executa uma instrução de E/S)
`P1 T` (Processo P1 termina)

O simulador deve processar esses comandos sequencialmente, simulando o comportamento do gerenciador de memória a cada passo.
