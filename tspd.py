import sys      # Necessário para ler info do terminal
import os       # Para ler todas as instâncias de uma pasta
import math     # Para cálculo de distâncias no plano euclidiano
import libs.GRASP as GRASP
import time     # Para verificar quanto tempo nossa solução consome
from libs.greedyRCL import greedypath_RCL
from libs.localSearch import localSearch2OPT # Vamos utilizar Metaheurística GRASP-VND para resolver TSP
from progress.bar import Bar # Para verificar o avanço da nossa resposta
from collections import namedtuple

from libs.utilities import calc_obj      # Para armazenar várias informações em um vértice

# tripla indicando o índice e coordenadas xy do cliente 
# cada vértice é representado por index
Node = namedtuple("Node", ['x', 'y', 'index'])

DEBUG = 0       # Variável global para debug do código.



def length(node1, node2):
    # Função que calcula distância euclidiana entre dois vértices do plano.
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)


def pass_comments(lines):
    # Função para ignorar comentários
    # das entradas da instância e tratar "/n".
    lines = lines.split('\n')
    num_input = []
    for line in lines:
        if not line.strip().startswith('/'):
            num_input.append(line)
    return num_input
    
def create_nodes(node_count, num_input):
    # Função para ler informações da entrada 
    # e criar nossas triplas que representam nós
    # no grafo.
    nodes = []
    for i in range(3, node_count + 3):
        line = num_input[i]
        parts = line.split()
        # Pré-processamento para se adequar aos nosso algoritmos
        if parts[2] == "depot":
            parts[2] = 0
        elif parts[2].find("v") != -1:
            parts[2] = parts[2].replace("v", "")
        elif parts[2].find("u") != -1:
            parts[2] = parts[2].replace("u", "")
        elif parts[2].find("loc") != -1:
            parts[2] = parts[2].replace("loc", "")
        nodes.append(
            Node(float(parts[0]), float(parts[1]), int(parts[2])))
    return nodes


def read_data(input_data):
    # Função para coletar informações da entrada.
    # Tratamento da entrada.
    numerical_input = pass_comments(input_data)

    # Coleta a velocidade do caminhão e drone.
    speed_truck = float(numerical_input[0])
    speed_drone = float(numerical_input[1])

    # Coleta a quantidade de vértices.
    node_count = int(float(numerical_input[2]))
    
    # Para o restante das linhas
    # Adiciona informações dos vértices nas triplas.
    nodes = create_nodes(node_count, numerical_input)

    if DEBUG >= 1:
        print(f"Velocidade do caminhão = {speed_truck}")
        print(f"Velocidade do drone = {speed_drone}")
        print(f"Número de vértices = {node_count}")
        
    if DEBUG >= 2:
        print("Lista de clientes:")
        for node in nodes:
            print(
                f"index do cliente = {node.index}, ({node.x}, {node.y})")
        print()

    return solve_tspd(node_count, nodes)


def solve_tspd(node_count, nodes):
    # TODO: Nessa função vamos resolver o problema do TSP-D,
    # por enquanto vamos testar o resultado do GRASP-VND do TSP nessas instâncias.
    start_time = time.time()
    node_indexes = []
    for node in nodes:
        node_indexes.append(node.index) 
    # Teste com algoritmo guloso aleatorizado
    # solution = greedypath_RCL(node_indexes, nodes, 0.25)
    # Teste com GRASP
    solution = GRASP.grasp_2opt(node_indexes, nodes)
    # Teste com GRASP-VND
    # solution = GRASP.grasp_vnd(node_indexes, nodes)
    
    # Calcula custo do TSP
    # TODO: Alterar para TSP-D
    cost_obj = calc_obj(solution, nodes)
    end_time = time.time()
    duration_time = end_time - start_time
    
    # Formata a solução obtida para escrevermos em um arquivo
    output_data = '%.2f' % cost_obj + '\n' + '%.2f' % duration_time + '\n'
    output_data += " ".join([str(solution[i]) for i in range(node_count)]) + '\n'

    return output_data

if __name__ == '__main__':
    # Função "main" seleciona o input na linha de comando.
    # Espera arquivos do tipo .txt e da pasta instâncias.
    # Roda todas as instâncias de um diretório ou um arquivo específico.
    # Formato:
    # python tspd.py "caminho diretorio/arquivo"
    # após resolução do problema
    # escreve em arquivo a solução obtida. 
    if len(sys.argv) > 1:
        count = 0
        path = sys.argv[1].strip()
        file_location = []
        if path.endswith(".txt"):
            count += 1
            file_location.append(f"{path}".strip())
        else:
            for file in os.listdir(path):
                if file.endswith(".txt"):
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        with Bar('Processing...', max=count) as bar:
            for file in file_location:
                with open(file, 'r') as input_data_file:
                    input_data = input_data_file.read()
                output_data = read_data(input_data)
                file = file.replace("instances", "solutions")
                file = file.split(".txt")
                solution_file = open(file[0].strip() + ".sol", "w")
                solution_file.write(output_data)
                solution_file.close()
                bar.next()
    else:
        print('This test requires an input file.  Please select one from the data directory. \
             (i.e. python tspd.py ./data/instances/singlecenter/singlecenter-1-n5.txt)')