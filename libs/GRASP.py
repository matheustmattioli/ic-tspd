import libs.greedyRCL as greedyRCL
import libs.localSearch as localSearch
import numpy as np
from adapter.adapt_tspd_author import calc_obj
from libs.ellipse import ellipse
from libs.spikes import spikes_tsp
from libs.split import make_tspd_sol

ALPHA_MAX = 0.5
N_ITE_GRASP = 5 # Number of iterations GRASP.
MAX_ITER_W_NO_IMPROV = 1

def grasp_vnd(cluster_vehicle, customers):
    # Greedy Randomized Adaptative Search Procedure (GRASP) implementation with 
    # Local Search 2-OPT and 3-OPT as "Search Procedure". 
    best_value = float('inf')
    ALPHA = 0
    n_iter_w_no_improv = 0
    t = 0 # see the number of iterations, for debug purposes.
    while ALPHA < ALPHA_MAX and n_iter_w_no_improv < MAX_ITER_W_NO_IMPROV:
        solution_vehicle = greedyRCL.greedypath_RCL(cluster_vehicle, customers, ALPHA)
        solution_vehicle, solution_obj = localSearch.localSearchVNS(solution_vehicle, customers)
        n_iter_w_no_improv += 1
        if solution_obj < best_value:
            best_value = solution_obj
            best_solution_vehicle = list(solution_vehicle)
            n_iter_w_no_improv = 0
            
        ALPHA += ALPHA_MAX/N_ITE_GRASP
        t += 1
    return best_solution_vehicle

def grasp_2opt(cluster_vehicle, customers):
    # Greedy Randomized Adaptative Search Procedure (GRASP) implementation with 
    # Local Search 2-OPT as "Search Procedure". 
    best_value = float('inf')
    ALPHA = 0
    n_iter_w_no_improv = 0
    t = 0 # see the number of iterations, for debug purposes.
    while ALPHA < ALPHA_MAX and n_iter_w_no_improv < MAX_ITER_W_NO_IMPROV:
        solution_vehicle = greedyRCL.greedypath_RCL(cluster_vehicle, customers, ALPHA)
        solution_vehicle, solution_obj = localSearch.localSearch2OPT(solution_vehicle, customers)
        n_iter_w_no_improv += 1
        if solution_obj < best_value:
            best_value = solution_obj
            best_solution_vehicle = list(solution_vehicle)
            n_iter_w_no_improv = 0
            
        ALPHA += ALPHA_MAX/N_ITE_GRASP
        t += 1
    return best_solution_vehicle

def grasp_tspd(node_count, nodes, speed_truck, speed_drone, tsp_choice):

    # TODO fazer grasp e testes
    # Para coleta de melhor solução global
    best_cost_obj = np.inf
    best_truck_nodes = []
    best_drone_nodes = []

    # Parâmetros GRASP
    alpha_grasp = 0
    n_iter_w_no_improv = 0

    # Array de rótulos dos nós.
    node_indexes = []
    for node in nodes:
        node_indexes.append(node.index)

    # GRASP para TSPD
    while alpha_grasp < ALPHA_MAX and n_iter_w_no_improv < MAX_ITER_W_NO_IMPROV:
        
        # Teste com algoritmo da estratégia de elipse
        if tsp_choice == 1:
            solution_tsp =  ellipse(node_indexes, nodes, 0.25, speed_drone, speed_truck)

        # Teste com heurística de formação de bicos
        if tsp_choice == 2:
            solution_tsp = spikes_tsp(node_indexes, nodes, speed_drone, 0.25)

        # Teste com GRASP
        if tsp_choice == 3:
            solution_tsp = grasp_2opt(node_indexes, nodes)
        
        # Teste com GRASP-VND
        if tsp_choice == 4:
            solution_tsp = grasp_vnd(node_indexes, nodes)

        # Tratamento para retornar o depósito para início do circuito.
        for depot_index in range(len(solution_tsp)):
            if solution_tsp[depot_index] == 0:
                solution_tsp = solution_tsp[depot_index:] + \
                    solution_tsp[:depot_index]
                break

        # Construção do grafo auxiliar e das entregas por drone
        solution_tspd, operations = make_tspd_sol(
            solution_tsp, speed_truck, speed_drone, nodes)

        # Separar as operacoes contidas em solution_tspd
        truck_nodes = solution_tspd[0]
        drone_nodes = solution_tspd[1]

        # TODO: Busca Local no TSP-D

        # Calcula custo do TSP-D
        cost_obj = calc_obj(operations, speed_truck, speed_drone, nodes)

        n_iter_w_no_improv += 1
        if cost_obj < best_cost_obj:
            best_cost_obj = cost_obj
            best_truck_nodes = list(truck_nodes)
            best_drone_nodes = list(drone_nodes)
            n_iter_w_no_improv = 0
            
        alpha_grasp += ALPHA_MAX/N_ITE_GRASP
    
    return best_cost_obj, best_truck_nodes, best_drone_nodes