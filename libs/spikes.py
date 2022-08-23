import libs.utilities as utilities
import numpy as np
import random

# Heurística construtiva para TSP.
# Comportamento Guloso-Aleatorizado.
def spikes_tsp(array_nodes, customers, ALPHA):

    # Objetivo é formar um circuito com a maior quantidade de "bicos" possível.
    # Isso é feito através da escolha do segundo vértice mais próximo do atual.
    size_circuit = len(array_nodes)
    best_obj = np.inf

    # Com range(1) a rota começa apenas no vértice 0, 
    # para outros valores em range, o algoritmo itera com 
    # a rota começando em outros vértices.
    for initial_node in range(1):
        dict_nodes = {array_nodes[i] : array_nodes[i] for i in range(size_circuit)}
        solution_spiked = [0 for i in range(size_circuit)]
        insert_position = 0
        solution_spiked[insert_position] = dict_nodes.pop(initial_node)
        insert_position += 1

        while insert_position < size_circuit:
            # Escolha gulosa aleatorizada com a RCL
            # RCL := Restricted Candidate List,
            # é definida pela equação: nearest_value + (furthest_value - nearest_value)*ALPHA
            # Decidir os dois vértices mais próximos do k atual e os dois mais distante
            nearest_value = np.inf
            second_nearest_value = np.inf   
            furthest_value = -np.inf
            second_furthest_value = -np.inf
            
            # Escolher vértice mais distante, segundo mais distante, 
            # mais próximo e segundo mais próximo.
            for candidate_node in array_nodes:
                if candidate_node in dict_nodes:
                    length_candidate_node = utilities.length(
                        customers[solution_spiked[insert_position - 1]], customers[candidate_node])
                    # Lógica para analisar vértice mais próximo e segundo mais próximo
                    if length_candidate_node < second_nearest_value:
                        if length_candidate_node < nearest_value:
                            # Se for o mais próximo, atualiza o antigo mais próximo para segundo 
                            # mais próximo.
                            second_nearest_value = nearest_value
                            
                            # Atualiza os valores para nearest value
                            nearest_value = length_candidate_node
                        else:
                            second_nearest_value = length_candidate_node
                    # Lógica para decidir vértice mais distante e segundo mais distante.
                    if length_candidate_node > second_furthest_value:
                        if length_candidate_node > furthest_value:
                            # Se for o mais distante, atualiza o antigo mais distante para segundo 
                            # mais distante.
                            second_furthest_value = furthest_value
                            
                            # Atualiza os valores para furthest value
                            furthest_value = length_candidate_node
                        else:
                            second_furthest_value = length_candidate_node
                        
            # A ideia é utilizar uma lista de candidatos mais próximo e segundo mais próximo.
            rcl_nearest_value = []
            rcl_second_nearest_value = []
            # Preencher a RCL
            for candidate_node in array_nodes:
                if candidate_node in dict_nodes:
                    length_candidate_node = utilities.length(
                        customers[solution_spiked[insert_position - 1]], customers[candidate_node])
                    # Verificar se o vértice está no range de valores do mais próximo ou do 
                    # segundo mais próximo.
                    if length_candidate_node <= nearest_value + (furthest_value - nearest_value)*ALPHA:
                        # Inserir o nó na rcl de mais próximos
                        rcl_nearest_value.append(candidate_node)
                    elif length_candidate_node <= second_nearest_value + (second_furthest_value - second_nearest_value)*ALPHA:
                        # Inserir o nó na rcl de segundo mais próximo
                        rcl_second_nearest_value.append(candidate_node)


            # Inserir o segundo vértice mais próximo primeiro em k + 1 e o mais próximo em k + 2
            # Repetir até que insert_position >= size_circuit
            if rcl_second_nearest_value:
                solution_spiked[insert_position] = random.choice(rcl_second_nearest_value)
                dict_nodes.pop(solution_spiked[insert_position])
                insert_position += 1
            if insert_position < size_circuit and rcl_nearest_value:
                solution_spiked[insert_position] = random.choice(rcl_nearest_value)
                dict_nodes.pop(solution_spiked[insert_position])
                insert_position += 1

        # Decidir o melhor circuito encontrado
        curr_obj = utilities.calc_obj(solution_spiked, customers)
        if curr_obj < best_obj:
            best_obj = curr_obj
            best_solution = solution_spiked
        dict_nodes.clear()
    return best_solution