from ctypes import util
import libs.utilities as utilities
import random

def spikes_tsp(circuit, customers):
    len_circuit = len(circuit)
    best_obj = float('inf')

    # Change range value to test circuit starting in dif nodes
    for v in range(1):
        dict_positions = {circuit[i] : circuit[i] for i in range(len_circuit)}
        solution_greedy = [0 for i in range(len_circuit)]
        k = 0
        solution_greedy[k] = dict_positions.pop(v)
        k += 1

        # Escolha gulosa
        while k < len_circuit:
            nearest_value = float('inf')
            second_nearest_value = float('inf')
            nearest_node = -1
            second_nearest_node = -1
            # Decidir os dois vértices mais próximos do k atual
            for n in circuit:
                if n in dict_positions:
                    length_N = utilities.length(customers[solution_greedy[k - 1]], customers[n])
                    # Lógica para analisar vértice mais próximo e segundo mais próximo
                    if length_N < second_nearest_value:
                        if length_N < nearest_value:
                            # Se for o mais próximo, atualiza o antigo mais próximo para segundo 
                            # mais próximo.
                            second_nearest_value = nearest_value
                            second_nearest_node = nearest_node
                            # Atualiza os valores para nearest value
                            nearest_value = length_N
                            nearest_node = n
                        else:
                            second_nearest_value = length_N
                            second_nearest_node = n
            
            # Inserir o segundo vértice mais próximo primeiro em k + 1 e o mais próximo em k + 2
            # Repetir até que k >= len_circuit
            if second_nearest_node != -1:
                solution_greedy[k] = second_nearest_node
                dict_positions.pop(solution_greedy[k])
                k += 1
            if k < len_circuit:
                solution_greedy[k] = nearest_node
                dict_positions.pop(solution_greedy[k])
                k += 1

        # Decidir o melhor circuito encontrado
        curr_obj = utilities.calc_obj(solution_greedy, customers)
        if curr_obj < best_obj:
            best_obj = curr_obj
            best_solution = solution_greedy
        dict_positions.clear()
    return best_solution