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
    nx.draw(G, pos=p, edge_color=color, node_size=10, width=2, node_color='black')  
    

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
    dictofpositions = {i : (nodes[i].x, nodes[i].y) for i in range(0, node_count)}      

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
    # TODO: Pegar as rotas dos drones.
    line = lines[1].split()     # Segunda linha armazena a rota do caminhão
    truck_route = list(map(int, line))
    
    # Desenha o TSP formado.
    graph_solution = nx.Graph()
    for i in range(0, node_count):
        graph_solution.add_node(i)
    for i in range(node_count):
        graph_solution.add_edge(truck_route[i], truck_route[(i + 1) % node_count])
    plt.figure(1)
    draw_graph(graph_solution, 'black', dictofpositions)
    dictofpositions = {}
    if DEBUG >= 3:
        print("Number of edges: ", graph_solution.number_of_edges())
        print("Number of nodes: ", graph_solution.number_of_nodes())

# Função "main" seleciona o input na linha de comando
if __name__ == '__main__':
    import sys
    # Função "main" seleciona o input na linha de comando
    # decide se roda todas as instâncias ou apenas uma específica
    # Formatos:
    # python tspd.py "info"
    # info pode ser:
    # Caminho da instância a ser executada.
    # 1 - Roda apenas DoubleCenter
    # 2 - Roda apenas SingleCenter
    # 3 - Roda apenas Uniform
    # 4 - Roda todas
    # após resolução do problema
    # escreve em arquivo a solução obtida. 
    if len(sys.argv) > 1:
        if sys.argv[1].strip() == "1":
            count = 0
            path = ".\\data\\solutions\\doublecenter"
            file_location = []
            for file in os.listdir(path):
                if file.endswith(".sol"):
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        elif sys.argv[1].strip() == "2":
            count = 0
            path = ".\\data\\solutions\\singlecenter"
            file_location = []
            for file in os.listdir(path):
                if file.endswith(".sol"):
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        elif sys.argv[1].strip() == "3":
            count = 0
            path = ".\\data\\solutions\\uniform"
            file_location = []
            for file in os.listdir(path):
                if file.endswith(".sol"):
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        elif sys.argv[1].strip() == "4": # Faça todos os passos anteriores
            count = 0
            path = ".\\data\\solutions\\doublecenter"
            file_location = []
            for file in os.listdir(path):
                if file.endswith(".sol"):
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
            
            path = ".\\data\\solutions\\singlecenter"
            for file in os.listdir(path):
                if file.endswith(".sol"):
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
            
            path = ".\\data\\solutions\\uniform"
            for file in os.listdir(path):
                if file.endswith(".sol"):
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        else:
            file_location = sys.argv[1].strip()
            # fazer pré-processamento adequado para tipo de solução
            # nossa ou do autor do dataset.
            if file_location.find("author-value") != -1:
                instance_file_location = file_location.replace("solutions", "instances")
                instance_file_location = instance_file_location.replace("-tsp-author-value", "")
                instance_file_location = instance_file_location.split(".sol")
                instance_file_location = instance_file_location[0] + ".txt"
            else:
                instance_file_location = file_location.replace("solutions", "instances")
                instance_file_location = instance_file_location.split(".sol")
                instance_file_location = instance_file_location[0] + ".txt"
            with open(instance_file_location, 'r') as input_data_file:
                input_data = input_data_file.read()
            read_data_sol(input_data, file_location)
            file_location = file_location.replace("solutions", "images")
            file_location = file_location.split(".sol")
            plt.savefig(file_location[0])
            sys.exit()
        with Bar('Processing...', max=count) as bar:
            for file in file_location:
                if file.find("author-value") != -1:
                    instance_file_location = file.replace("solutions", "instances")
                    instance_file_location = instance_file_location.replace("-tsp-author-value", "")
                    instance_file_location = instance_file_location.split(".sol")
                    instance_file_location = instance_file_location[0] + ".txt"
                else:
                    instance_file_location = file.replace("solutions", "instances")
                    instance_file_location = instance_file_location.split(".sol")
                    instance_file_location = instance_file_location[0] + ".txt"
                with open(instance_file_location, 'r') as input_data_file:
                    input_data = input_data_file.read()
                read_data_sol(input_data, file)
                file = file.replace("solutions", "images")
                file = file.split(".sol")
                plt.savefig(file[0])
                plt.clf()
                bar.next()
    else:
        print('This test requires an input file.  Please select one from the data directory.' \
             '(i.e. python print_nodes.py ./data/solutions/singlecenter/singlecenter-1-n5.sol)')
    