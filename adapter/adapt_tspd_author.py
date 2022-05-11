from itertools import count
from platform import node
import sys
from collections import namedtuple
from time import time
from numpy import double
from progress.bar import Bar
import os
import math
# import datetime

Node = namedtuple("Node", ['x', 'y', 'index'])


def calc_time_edge(node1, node2, speed):
    # Função para calcular o tempo de viajem em uma aresta   
    return (math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2))/speed

def calc_cost(tour, speed, nodes):
    # vamos calcular o tempo consumido pelo tour do caminhão ou drone
    time = 0
    for i in range(1, len(tour)):
        time += calc_time_edge(nodes[tour[i - 1]], nodes[tour[i]], speed)
    return time

def calc_cost_operation(truck_nodes, drone_nodes, speed_truck, speed_drone, nodes):
    # vamos calcular o tempo consumido por cada operação
    if len(drone_nodes) > 0:
        cost_truck_route = calc_cost(truck_nodes, speed_truck, nodes)
        cost_drone_route = calc_cost(drone_nodes, speed_drone, nodes)
        cost = max(cost_truck_route, cost_drone_route)
    else:
        cost = calc_cost(truck_nodes, speed_truck, nodes)
    return cost

def calc_obj(operations, speed_truck, speed_drone, nodes):
    # vamos calcular a função objetivo do problema
    cost_obj = 0
    for i in range(len(operations)):
        truck_nodes = operations[i][0]
        drone_nodes = operations[i][1]
        cost_obj += calc_cost_operation(truck_nodes, drone_nodes, speed_truck, speed_drone, nodes)
    return cost_obj

def pass_comments(lines):
    # Função para ignorar comentários
    # das entradas da instância e tratar "/n".
    lines = lines.split('\n')
    num_input = []
    for line in lines:
        if not line.strip().startswith('/'):
            num_input.append(line)
    return num_input

def create_nodes(node_count, file_location):
    # Função para ler informações da entrada 
    # e criar nossas triplas que representam nós
    # no grafo.
    file_location = file_location.replace("author_solutions", "")
    file_location = file_location.replace("-sMIP", "")
    with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
    lines = pass_comments(input_data)
    speed_truck = 1/float(lines[0])
    speed_drone = 1/float(lines[1])
    # print("speed_truck = ", speed_truck)
    # print("speed_drone = ", speed_drone)
    nodes = []
    for i in range(3, node_count + 3):
        line = lines[i]
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
    return nodes, speed_truck, speed_drone

def verify_sol(input_data, file_location):
    # Função para coletar soluçao do autor.
    # Tratamento da entrada.
    sol_auth = pass_comments(input_data)
    # Primeira posiçao do arquivo armazena qtd de vértices.
    count_operation = int(sol_auth[0])
    
    # Coleta as informaçoes correspendentes à essa instância.
    nodes, speed_truck, speed_drone = create_nodes(count_operation, file_location)
    
    # Construir o tour da solução do autor
    operations = []
    
    for i in range(1, count_operation + 1):
        line = sol_auth[i]
        parts = line.split()
        start = int(parts[0])
        end = int(parts[1])
        drone_node = int(parts[2])
        # if drone_node == -1:
        #     continue
        internal_nodes = int(parts[3])
        truck_nodes = [start]
        for j in range(4, internal_nodes + 4):
            truck_nodes.append(int(parts[j]))
        if truck_nodes[internal_nodes] != end:
            if truck_nodes[internal_nodes] == 0:
                truck_nodes.pop(internal_nodes)
            else:
                truck_nodes.append(end)
        if drone_node > 0:
            drone_nodes = [start, drone_node, end]
        else:
            drone_nodes = []
        operations.append([truck_nodes, drone_nodes])
    
    # Debug
    print("count_operation =", count_operation)
    for i in range(count_operation):
        print(nodes[i].index, nodes[i].x, nodes[i].y)
    print("operations =", operations)
    print("speed_truck_verify_sol =", speed_truck)
    print("speed_drone_verify_sol =", speed_drone)
    
    return calc_sol(count_operation, nodes, operations, speed_truck, speed_drone)

def calc_sol(count_operation, nodes, operations, speed_truck, speed_drone):
    # Nessa função é calculado o custo da solução
    # obtida pelo autor do dataset
    cost_obj = float(calc_obj(operations, speed_truck, speed_drone, nodes))
    print("cost_obj = ", cost_obj)

    # TODO: formar os circuitos do caminhão e drone
    # # Construir Truck Tour e Drone Tour a partir de operations
    # truck_tour = [] # Podemos ter mais de um circuito por caminhão
    # drone_tour = [] # Os triangulos formados pelo drone
    # tour_aux = []   # Vetor auxiliar para construçao da truck_tour

    # for op in operations:
    #     # Tours do drone
    #     drone_tour.append(op[1])
    #     # Tours do caminhao
    #     tour_residuo = tour_aux # Armazena o circuito em construção pelas iterações
    #     tour_aux = op[0]
    #     first_node = tour_aux[0]
    #     # Se o primeiro nó for igual ao último, o tour está completo.
    #     # E se o tamanho for 2 significa que o caminhao ficou estacionado, portanto não fecha um circuito.
    #     if first_node == tour_aux[len(tour_aux) - 1] and len(tour_aux) > 2: 
    #         truck_tour.append(tour_aux)
    #         tour_residuo = []
    #     else:
    #         for i in range(len(tour_residuo)):
    #             tour_aux.append(tour_residuo[i])

  
    # tempo do tour no output data
    output_data = '%.2f' % cost_obj + '\n'

    # TODO: formar os circuitos do caminhão e drone
    # output_data += " ".join([str(tour[i]) for i in range(node_count)]) + '\n'

    return output_data


if __name__ == '__main__':
    # Função "main" seleciona o input na linha de comando.
    # Espera arquivos do tipo .txt e da pasta instâncias/x/author_solutions.
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
                if file.endswith(".txt") and file.find("tsp") == -1:
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        with Bar('Processing...', max=count) as bar:
            for file in file_location:
                with open(file, 'r') as input_data_file:
                    input_data = input_data_file.read()
                output_data = verify_sol(input_data, file)
                file = file.replace("instances", "solutions") 
                file = file.replace("author_solutions", "")
                file = file.split(".txt")
                solution_file = open(file[0] + "-author-value" + ".sol", "w")
                solution_file.write(output_data)
                solution_file.close()
                bar.next()
    else:
        print('This test requires an input file.  Please select one from the data directory. \
             (i.e. python solver.py ./data/instances/singlecenter/author_solutions/singlecenter-1-n5-tsp.txt)')