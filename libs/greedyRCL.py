import libs.utilities as utilities
import random


def greedypath_RCL(circuit, customers, ALPHA):
    # Constuctive heuristic for Traveling Salesman Problem (TSP).
    # It's a nearest neighbour (NN) algorithm with Restricted Candidate List (RCL).
    # Do hamiltonian circuit with greedy choices in selected subset
    # Selected by clusters function
    # using RCL
    len_circuit = len(circuit)
    obj_BS = float('inf')
    
    # Change range value to test circuit  starting in dif nodes
    for v in range(1):
        dict_positions = {circuit[i] : circuit[i] for i in range(len_circuit)}
        solution_greedy = [0 for i in range(len_circuit)]
        k = 0
        solution_greedy[k] = dict_positions.pop(v)
        k += 1
        # greedy choices
        while k < len_circuit: 
            nearest_value = float('inf')
            farthest_value = 0
            # deciding nearest and farthest customers from  k - 1 customer
            for n in circuit:
                if n in dict_positions:
                    length_N = utilities.length(customers[solution_greedy[k - 1]], customers[n])
                    if length_N < nearest_value:
                        nearest_value = length_N
                    if length_N > farthest_value:
                        farthest_value = length_N
            RCL = []
            # filling in RCL
            for n in circuit:
                if n in dict_positions:
                    length_N = utilities.length(customers[solution_greedy[k - 1]], customers[n])
                    if length_N <= (nearest_value + (farthest_value - nearest_value)*ALPHA): # Condition to insert neighbours in RCL
                        RCL.append(n)
            solution_greedy[k] = random.choice(RCL)
            dict_positions.pop(solution_greedy[k])
            k += 1
        # Decide best solution found
        curr_obj = utilities.calc_obj(solution_greedy, customers)
        if curr_obj < obj_BS:
            obj_BS = curr_obj
            best_solution = solution_greedy
        dict_positions.clear()
    return best_solution