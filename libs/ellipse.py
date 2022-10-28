import random
from re import I
from turtle import speed
import libs.utilities as utilities
import numpy as np

# Heurística construtiva para TSP.
# Comportamento Guloso-Aleatorizado.
def ellipse(array_nodes, customers, ALPHA, drone_speed, truck_speed):

    # Formar um circuito com vértices interessantes para entregas por drone,
    # para isso vamos selecionar vértices em uma vizinhança em formato de "elipse" 
    # para serem colocadas na Lista Restrita de Candidatos (RCL).
    size_circuit = len(array_nodes)
    dict_nodes = {array_nodes[i] : array_nodes[i] for i in range(size_circuit)}
    solution_ellipse = [0 for i in range(size_circuit)]
    insert_position = 0
    solution_ellipse[insert_position] = dict_nodes.pop(0)
    insert_position += 1

    # Fixar uma seed para testes
    # random.seed(4542355562136458828)
    
    while insert_position < size_circuit:
        # Os membros da RCL são escolhidos de acordo com um valor
        # relacionado com a distância máxima percorrida pelo drone  
        # enquanto o caminhão vai até o nó mais próximo

        nearest_value = np.inf
        furthest_value = -np.inf
        
        # Escolher vértice mais distante, segundo mais distante, 
        # mais próximo e segundo mais próximo.
        for candidate_node in array_nodes:
            if candidate_node in dict_nodes:
                length_candidate_node = utilities.length(
                    customers[solution_ellipse[insert_position - 1]], customers[candidate_node])
                # Lógica para analisar vértice mais próximo
                if length_candidate_node < nearest_value:
                    nearest_value = length_candidate_node
                # Escolher o vértice mais distante.
                if length_candidate_node > furthest_value:
                    # Atualiza os valores para furthest value
                    furthest_value = length_candidate_node

        # RCL com nós em uma distância elíptica do nó atual.
        rcl = []

         # Preencher a RCL
        for candidate_node in array_nodes:
            if candidate_node in dict_nodes:
                length_candidate_node = utilities.length(
                    customers[solution_ellipse[insert_position - 1]], customers[candidate_node])
                # Verificar se o vértice está no range de valores da RCL segundo a equação:
                # nearest + (furthest - nearest)*ALPHA 
                if length_candidate_node <= (nearest_value + (furthest_value - nearest_value)*ALPHA):
                    # Inserir o nó na rcl 
                    rcl.append(candidate_node)
        

        # Distancia do nó analisado para origem e destino.
        # Cálculo dessa rcl:
        # dist_orig + dist_dest <= nearest_value*(drone_speed/truck_speed)*(1 + ALPHA)
        # Caso essa rcl seja vazia, insira apenas o dest_node.
        
        orig_node = solution_ellipse[insert_position - 1]
        dest_node = random.choice(rcl)
        dict_nodes.pop(dest_node)
        rcl_ellipse = []

        # Preencher a rcl_ellipse 
        for candidate_node in array_nodes:
            if candidate_node in dict_nodes:
                dist_orig = utilities.length(
                    customers[orig_node], customers[candidate_node])
                dist_dest = utilities.length(
                    customers[dest_node], customers[candidate_node]
                )
                # Verifica se está na elipse
                if dist_orig + dist_dest <= nearest_value*(drone_speed/truck_speed)*(1 + ALPHA):
                    # Inserir o nó na rcl_ellipse 
                    rcl_ellipse.append(candidate_node)

        # Inserir um nó da elipse e depois o nó destino
        if rcl_ellipse:
            random.shuffle(rcl_ellipse)
            solution_ellipse[insert_position] = rcl_ellipse.pop()
            dict_nodes.pop(solution_ellipse[insert_position])
            insert_position += 1
            solution_ellipse[insert_position] = dest_node
        else:
            solution_ellipse[insert_position] = dest_node
        insert_position += 1
   
    dict_nodes.clear()

    return solution_ellipse

