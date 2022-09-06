import libs.utilities as utilities
import numpy as np
import random

# Heurística construtiva para TSP.
# Comportamento Guloso-Aleatorizado.
def spikes_tsp(array_nodes, customers, speed_drone, ALPHA):

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
                    # Escolher o vértice mais distante.
                    if length_candidate_node > furthest_value:
                        # Atualiza os valores para furthest value
                        furthest_value = length_candidate_node
                        
            # A ideia é utilizar uma lista de candidatos utilizando mais próximo e segundo mais próximo no calculo.
            rcl = []
    
            # Preencher a RCL
            for candidate_node in array_nodes:
                if candidate_node in dict_nodes:
                    length_candidate_node = utilities.length(
                        customers[solution_spiked[insert_position - 1]], customers[candidate_node])
                    # Verificar se o vértice está no range de valores da RCL segundo a equação:
                    # second_nearest + (furthest - second_nearest)*ALPHA 
                    # Cálculo só funciona se houver um second_nearest...
                    # Tratando o caso em que não existe second_nearest
                    if second_nearest_value == np.inf:
                        second_nearest_value = nearest_value

                    # Testar com if abaixo.
                    # if length_candidate_node <= (nearest_value + (furthest_value - nearest_value)*ALPHA)*(speed_drone/2):
                    if length_candidate_node <= nearest_value + (furthest_value - nearest_value) * ALPHA or length_candidate_node <= nearest_value * (speed_drone/2):
                    # if length_candidate_node <= second_nearest_value + (furthest_value - second_nearest_value)*ALPHA:
                        # Inserir o nó na rcl 
                        rcl.append(candidate_node)
            
            # Sortear dois pontos da RCL e inserir o mais distante primeiro (fazer a verificação)
        
            random.shuffle(rcl)
            candidate_node1 = rcl.pop()
            # Se houverem elementos na lista e a próxima posição a ser inserido não estoura o tamanho do circuito
            if rcl and (insert_position + 1) < size_circuit:
                candidate_node2 = rcl.pop()
                # Distância de cada um para o nó atual
                length_candidate_node1 = utilities.length(
                    customers[candidate_node1], customers[solution_spiked[insert_position - 1]]
                )
                length_candidate_node2 = utilities.length(
                    customers[candidate_node2], customers[solution_spiked[insert_position - 1]]
                )
                if length_candidate_node1 > length_candidate_node2:
                    solution_spiked[insert_position] = candidate_node1
                    dict_nodes.pop(candidate_node1)
                    insert_position += 1
                    solution_spiked[insert_position] = candidate_node2
                    dict_nodes.pop(candidate_node2)
                    insert_position += 1
                else:
                    solution_spiked[insert_position] = candidate_node2
                    dict_nodes.pop(candidate_node2)
                    insert_position += 1
                    solution_spiked[insert_position] = candidate_node1
                    dict_nodes.pop(candidate_node1)
                    insert_position += 1
            else:
                solution_spiked[insert_position] = candidate_node1
                dict_nodes.pop(candidate_node1)
                insert_position += 1


        # Decidir o melhor circuito encontrado
        curr_obj = utilities.calc_obj(solution_spiked, customers)
        if curr_obj < best_obj:
            best_obj = curr_obj
            best_solution = solution_spiked
        dict_nodes.clear()
    return best_solution