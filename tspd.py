import sys      # Necessário para ler info do terminal
import math     # Para cálculo de distâncias no plano euclidiano
from collections import namedtuple      # Para armazenar várias informações em um vértice

# tripla indicando o índice e coordenadas xy do cliente 
# cada vértice é representado por index
Node = namedtuple("Node", ['x', 'y', 'index'])

DEBUG = 0       # Variável global para debug do código.



def length(node1, node2):
    # Função que calcula distância euclidiana entre dois vértices do plano.
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

def read_data(input_data):
    # Recebe os dados da instância e formata para uso nas funções

    # Lê as linhas da nossa entrada
    lines = input_data.split('\n')
    
    # Coleta informação da primeira linha
    node_count = int(lines[0])      # Qtd vértices
    
    # Para o restante das linhas
    # Adiciona informações dos vértices nas triplas
    nodes = []
    for i in range(1, node_count + 1):
        line = lines[i]
        parts = line.split()
        nodes.append(
            Node(float(parts[0]), float(parts[1]), int(parts[2])))

    if DEBUG >= 1:
        print(f"Numero de vértices = {node_count}")
        
    if DEBUG >= 2:
        print("Lista de clientes:")
        for node in nodes:
            print(
                f"index do cliente = {node.index}, ({node.x}, {node.y})")
        print()

    return solve_tspd(node_count, nodes)

# TODO: Nessa função vamos resolver o problema do TSP-D,
# por enquanto vamos testar apenas uma ideia de heurística aleatorizada 
def solve_tspd(node_count, nodes):

    solution = nodes        # Solução trivial

    # Calcula custo do TSP
    # TODO: Alterar para TSP-D e modularizar
    cost_obj = 0
    for i in range(node_count):
        cost_obj += length(solution[i], solution[(i + 1) % node_count])

    # Formata a solução obtida para escrevermos em um arquivo
    output_data = '%.2f' % cost_obj + '\n'
    output_data += " ".join([str(solution[i].index) for i in range(node_count)]) + '\n'

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
        solution_file = open(file_location + ".sol", "w")
        solution_file.write(output_data)
        solution_file.close()
    else:
        print('This test requires an input file.  Please select one from the data directory. \
             (i.e. python solver.py ./data/instances/tspd_5_1)')