from itertools import count
import sys
from collections import namedtuple
from progress.bar import Bar
import os
import math

Node = namedtuple("Node", ['x', 'y', 'index'])


def length(node1, node2):
    # Função que calcula distância euclidiana entre dois vértices do plano.
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

def calc_obj(tour, nodes):
    cost_obj = 0
    for i in range(len(tour)):
        cost_obj += length(nodes[tour[i - 1]], nodes[tour[i]])
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
    file_location = file_location.replace("-tsp", "")
    with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
    lines = pass_comments(input_data)
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
    return nodes

def verify_sol(input_data, file_location):
    # Função para coletar soluçao do autor.

    # Tratamento da entrada.
    sol_auth = pass_comments(input_data)
    # Primeira posiçao do arquivo armazena qtd de vértices.
    node_count = int(float(sol_auth[0]))
    
    # Coleta as informaçoes correspendentes à essa instância.
    nodes = create_nodes(node_count, file_location)

    # Construir o tour da solução do autor
    tour = []
    for i in range(1, node_count + 1):
        line = sol_auth[i]
        parts = line.split()
        tour.append(int(parts[0]))

    return calc_sol(node_count, nodes, tour)

def calc_sol(node_count, nodes, tour):
    # Nessa função é calculado o custo da solução
    # obtida pelo autor do dataset
    
    cost_obj = calc_obj(tour, nodes)
    
    output_data = '%.2f' % cost_obj + '\n'
    output_data += " ".join([str(tour[i]) for i in range(node_count)]) + '\n'

    return output_data


if __name__ == '__main__':
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
            path = ".\\data\\instances\\doublecenter\\author_solutions"
            file_location = []
            for file in os.listdir(path):
                if file.endswith(".txt") and file.find("sMIP") == -1:
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        elif sys.argv[1].strip() == "2":
            count = 0
            path = ".\\data\\instances\\singlecenter\\author_solutions"
            file_location = []
            for file in os.listdir(path):
                if file.endswith(".txt") and file.find("sMIP") == -1:
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        elif sys.argv[1].strip() == "3":
            count = 0
            path = ".\\data\\instances\\uniform\\author_solutions"
            file_location = []
            for file in os.listdir(path):
                if file.endswith(".txt") and file.find("sMIP") == -1:
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        elif sys.argv[1].strip() == "4": # Faça todos os passos anteriores
            count = 0
            path = ".\\data\\instances\\doublecenter\\author_solutions"
            file_location = []
            for file in os.listdir(path):
                if file.endswith(".txt") and file.find("sMIP") == -1:
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
            
            path = ".\\data\\instances\\singlecenter\\author_solutions"
            for file in os.listdir(path):
                if file.endswith(".txt") and file.find("sMIP") == -1:
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
            
            path = ".\\data\\instances\\uniform\\author_solutions"
            for file in os.listdir(path):
                if file.endswith(".txt") and file.find("sMIP") == -1:
                    count += 1
                    file_location.append(f"{path}\{file}".strip())
        else:
            file_location = sys.argv[1].strip()
            with open(file_location, 'r') as input_data_file:
                input_data = input_data_file.read()
            output_data = verify_sol(input_data, file_location)
            file_location = file_location.replace("instances", "solutions") 
            file_location = file_location.replace("author_solutions", "")
            file_location = file_location.split(".txt")
            solution_file = open(file_location[0] + "-author-value" + ".sol", "w")
            solution_file.write(output_data)
            solution_file.close()
            sys.exit()
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