#!/usr/bin/python
# -*- coding: utf-8 -*-
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
    

def read_instance(input_data, file_location):
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

    dictofpositions = {i : (nodes[i].x, nodes[i].y) for i in range(0, node_count)}      # Armazena as coordenadas
                                                                                                    # do vértice i

    
    # Por fim, podemos mandar imprimir a solução
    read_sol(node_count, nodes, dictofpositions, file_location)


def read_sol(node_count, nodes, dictofpositions, file_location):

    # As próximas linhas realiza a leitura
    # do tour construído para TSP
    # TODO: Adaptar para TSP-D
    file_location = file_location.replace("instances", "solutions") 
    instance_sol_file = open(file_location + ".sol", "r")
    
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
    
    if DEBUG >= 3:
        print("Number of edges: ", graph_solution.number_of_edges())
        print("Number of nodes: ", graph_solution.number_of_nodes())

# Função "main" seleciona o input na linha de comando
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        read_instance(input_data, file_location)
    else:
        print('This test requires an input file.  Please select one from the data directory.' \
             '(i.e. python print_nodes.py ./data/instances/tspd_5_1)')
    file_location = file_location.replace("instances", "images")
    plt.savefig(file_location)
    plt.show()