from classesProcessos import *
from memoriaPrincipal import *

# "With" é uma palavra reservada que garante o gerenciamento de recursos,
# abrindo e fechando o arquivo de uma vez só
with open("caso_de_teste.txt", "r", encoding="utf-8") as f:
    # Em python, podemos criar tuplas de vários tamanhos e com itens de vários tipos diferentes,
    # a ideia é retornar uma tupla em que:
    #   - O primeiro item (seqComandos[0]) é o nome do processo
    #   - O segundo (seqComandos[1]) é o comando a ser operado
    #   - As demais variam dependendo do comando
    #
    # seqComandos tem esse formato: [('P3', 'C', '800'), ('P3', 'R', '100'), ('P3', 'P', '150'), ('P3', 'W', '110'), ..., ('P4', 'T')]
    seqComandos = f.read()
    seqComandos = [tuple(c.split(" ")) for c in seqComandos.split("\n")]

mp = MemoriaPrincipal(TAM_MEMORIA)

processosLista = []
for com in seqComandos:
    # TODO: Conforme o código crescer e tomar forma, adicionemos novos casos
    # (possivelmente tornar esse if em um switch case com as instruções possíveis)
    if com[1] == "C":
        idProcesso = int(com[0][1])
        tamProcesso = int(com[2])
        try:
            unidade = com[3]
            match unidade:
                case "KB":
                    tamProcesso *= 2**10
                case "MB":
                    tamProcesso *= 2**20
                case "GB":
                    tamProcesso *= 2**30
                case _:
                    pass
        except IndexError:
            # Evitar erro no eventual caso de não passar unidade de tamanho
            pass
        processosLista.append(Processo(idProcesso, tamProcesso))

for p in processosLista:
    print(p.id)
    print(p.tamanho)
    print(p.qtdPaginas)