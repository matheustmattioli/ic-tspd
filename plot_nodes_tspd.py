# Script para plotar o grafo formado pelos nossos resultados
import sys
import os
from progress.bar import Bar
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import write_dot
from collections import namedtuple

# tripla indicando o índice e coordenadas xy do cliente
# cada vértice é representado por index
Node = namedtuple("Node", ['x', 'y', 'index'])

DEBUG = 0


def draw_graph(G, color, p):
    # Realiza o plot do grafo formado
    nx.draw(G, pos=p, edge_color=color, node_size=10,
            width=2, node_color='black')


def read_data_sol(input_data, file_location):
    # Lê as linhas da nossa entrada

    lines = input_data.split('\n')

    numerical_input = []
    # Ignorar os comentários
    for line in lines:
        if not line.strip().startswith('/'):
            numerical_input.append(line)

    # Coleta a velocidade do caminhão e drone
    speed_truck = float(numerical_input[0])
    speed_drone = float(numerical_input[1])
    # Coleta a quantidade de vértices
    node_count = int(float(numerical_input[2]))

    # Para o restante das linhas
    # Adiciona informações dos vértices nas triplas
    nodes = []
    for i in range(3, node_count + 3):
        line = numerical_input[i]
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

    # Armazena as coordenadas do vértice i
    dictofpositions = {i: (nodes[i].x, nodes[i].y)
                       for i in range(0, node_count)}

    # Por fim, podemos mandar imprimir a solução
    plot_sol(node_count, nodes, dictofpositions, file_location)


def plot_sol(node_count, nodes, dictofpositions, file_location):
    # As próximas linhas realizam a leitura
    # do tour construído para TSP
    # TODO: Adaptar para TSP-D

    instance_sol_file = open(file_location, "r")

    # TODO: Ainda é necessário adaptar a separação em
    # uma lista de clientes atendidos por drone e
    # outra por caminhões.
    solution_data = instance_sol_file.read()
    instance_sol_file.close()

    # Separa as linhas em várias listas.
    lines = solution_data.split('\n')

    # A primeira Linha contém o custo da solução.
    first_line = lines[0].split()
    sol_value = float(first_line[0])

    # Pegamos a rota do caminhão.
    line = lines[2].split()     # Terceira linha armazena a rota do caminhão
    truck_route = list(map(int, line))

    # Rotas do Drone
    drones_deliveries = []
    for i in range(3, len(lines)):
        line = lines[i].split()
        drone_delivery = list(map(int, line))
        drones_deliveries.append(drone_delivery)

    # Desenha o TSP formado.
    graph_solution_truck = nx.Graph()
    graph_solution_drone = nx.Graph()
    for i in range(0, node_count):
        graph_solution_truck.add_node(i)
        graph_solution_drone.add_node(i)
    for i in range(len(truck_route)):
        graph_solution_truck.add_edge(
            truck_route[i], truck_route[(i + 1) % len(truck_route)])
    for dd in drones_deliveries:
        if len(dd) > 0:
            graph_solution_drone.add_edge(dd[0], dd[1])
            graph_solution_drone.add_edge(dd[1], dd[2])
    plt.figure(1)
    draw_graph(graph_solution_truck, 'black', dictofpositions)
    nx.draw(graph_solution_drone, pos=dictofpositions, edge_color='black',
            node_size=10, width=2, node_color='black', style='dashed')
    dictofpositions = {}


# Função "main" seleciona o input na linha de comando
# Espera arquivos do tipo .sol
if __name__ == '__main__':
    import sys
    # Função "main" seleciona o input na linha de comando
    # roda todas as instâncias de um diretório ou um arquivo específico
    # Formato:
    # python tspd.py "caminho diretorio/arquivo"
    # após resolução do problema
    # escreve em arquivo a solução obtida.
    if len(sys.argv) > 1:
        count = 0
        path = sys.argv[1].strip()
        file_location = []
        if path.endswith(".sol"):
            count += 1
            file_location.append(f"{path}".strip())
        else:
            for file in os.listdir(path):
                if file.endswith(".sol") and not "author" in file:
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        with Bar('Processing...', max=count) as bar:
            for file in file_location:
                if file.find("author-value") != -1:
                    instance_file_location = file.replace(
                        "solutions", "instances")
                    instance_file_location = instance_file_location.replace(
                        "-tsp-author-value", "")
                    instance_file_location = instance_file_location.split(
                        ".sol")
                    instance_file_location = instance_file_location[0] + ".txt"
                else:
                    instance_file_location = file.replace(
                        "solutions", "instances")
                    instance_file_location = instance_file_location.split(
                        ".sol")
                    instance_file_location = instance_file_location[0] + ".txt"
                with open(instance_file_location, 'r') as input_data_file:
                    input_data = input_data_file.read()
                read_data_sol(input_data, file)
                file = file.replace("solutions", "images")
                file = file.split(".sol")
                plt.show()
                plt.savefig(file[0])
                plt.clf()
                bar.next()
    else:
        print('This test requires an input file.  Please select one from the data directory.'
              '(i.e. python print_nodes.py ./data/solutions/singlecenter/singlecenter-1-n5.sol)')
