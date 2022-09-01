import random
from turtle import speed
import libs.utilities as utilities
import numpy as np

# Heurística construtiva para TSP.
# Comportamento Guloso-Aleatorizado.
def ellipse(array_nodes, customers, ALPHA, drone_speed):

    # Formar um circuito com vértices interessantes para entregas por drone,
    # para isso vamos selecionar vértices em uma vizinhança em formato de "elipse" 
    # para serem colocadas na Lista Restrita de Candidatos (RCL).
    size_circuit = len(array_nodes)
    dict_nodes = {array_nodes[i] : array_nodes[i] for i in range(size_circuit)}
    solution_ellipse = [0 for i in range(size_circuit)]
    insert_position = 0
    solution_ellipse[insert_position] = dict_nodes.pop(random.choice(array_nodes))
    insert_position += 1

    while insert_position < size_circuit:
        # Os membros da RCL são escolhidos de acordo com um valor
        # relacionado com a distância máxima percorrida pelo drone  
        # enquanto o caminhão vai até o nó mais próximo

        nearest_value = np.inf
        nearest_node = -1
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
                    nearest_node = candidate_node
                # Escolher o vértice mais distante.
                if length_candidate_node > furthest_value:
                    # Atualiza os valores para furthest value
                    furthest_value = length_candidate_node

        # RCL com nós em uma distância elíptica do nó atual.
        rcl_ellipse = []

        # Calcular distância máxima percorrida pelo drone
        # enquanto o caminhão viaja para o nó mais próximo.
        speed_truck = 1
        truck_distance = nearest_value*speed_truck
        drone_distance = (truck_distance/2)*speed

        # Preencher a RCL
        for candidate_node in array_nodes:
            if candidate_node in dict_nodes:
                length_candidate_node = utilities.length(
                    customers[solution_ellipse[insert_position - 1]], customers[candidate_node])
                # Verifica se está na "elipse"
                # O ALPHA utilizado é uma constante para tolerância de atraso.
                if length_candidate_node <= drone_distance*ALPHA:
                    # Inserir o nó na rcl 
                    rcl_ellipse.append(candidate_node)

        solution_ellipse[insert_position] = nearest_node
        dict_nodes.pop(nearest_node)
        insert_position += 1
        if nearest_node in rcl_ellipse:
            rcl_ellipse.remove(nearest_node)
        if rcl_ellipse and insert_position < size_circuit:
            solution_ellipse[insert_position] = random.choice(rcl_ellipse)
            dict_nodes.pop(solution_ellipse[insert_position])
            insert_position += 1
    dict_nodes.clear()

    return solution_ellipse

