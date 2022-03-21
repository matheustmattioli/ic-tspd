import sys      # Necessário para ler info do terminal
import math     # Para cálculo de distâncias no plano euclidiano
import libs.GRASP as GRASP # Vamos utilizar Metaheurística GRASP-VND para resolver TSP
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
        else:
            parts[2] = parts[2].replace("v", "")
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

    node_indexes = []
    for node in nodes:
        node_indexes.append(node.index) 
    solution = GRASP.grasp_vnd(node_indexes, nodes)       

    
    # Calcula custo do TSP
    # TODO: Alterar para TSP-D
    cost_obj = calc_obj(solution, nodes)
    
    # Formata a solução obtida para escrevermos em um arquivo
    output_data = '%.2f' % cost_obj + '\n'
    output_data += " ".join([str(solution[i]) for i in range(node_count)]) + '\n'

    return output_data

if __name__ == '__main__':
    # Função "main" seleciona o input na linha de comando
    # após resolução do problema
    # escreve em arquivo a solução obtida. 
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        output_data = read_data(input_data)
        print(output_data)
        file_location = file_location.replace("instances", "solutions") 
        file_location = file_location.split(".txt")
        solution_file = open(file_location[0] + ".sol", "w")
        solution_file.write(output_data)
        solution_file.close()
    else:
        print('This test requires an input file.  Please select one from the data directory. \
             (i.e. python solver.py ./data/instances/singlecenter/singlecenter-1-n5.txt)')