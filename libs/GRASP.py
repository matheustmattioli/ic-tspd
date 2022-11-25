import time
import libs.greedyRCL as greedyRCL
import libs.utilities as utils
import numpy as np
import random
from adapter.adapt_tspd_author import calc_obj
from libs.ellipse import ellipse
from libs.spikes import spikes_tsp
from libs.split import make_tspd_sol

ALPHA_MAX = 0.2
N_ITE_GRASP = 10 # Number of iterations GRASP.
MAX_ITER_W_NO_IMPROV = 10
epsilon = 0.001
# Seed para testes
random.seed(4542355562136458828)


def nearest(cluster_vehicle, customers, alpha):
    solution_vehicle, _ = greedyRCL.greedypath_RCL(cluster_vehicle, customers, alpha)
    
    return solution_vehicle

def grasp_tspd(node_count, nodes, speed_truck, speed_drone, tsp_choice):

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
    while alpha_grasp <= ALPHA_MAX + epsilon and n_iter_w_no_improv < MAX_ITER_W_NO_IMPROV:
        
        # print("\nalpha_grasp = ", alpha_grasp)
        # Teste com algoritmo da estratégia de elipse
        if tsp_choice == 1:
            solution_tsp = ellipse(node_indexes, nodes, alpha_grasp, speed_drone, speed_truck)

        # Teste com heurística de formação de bicos
        if tsp_choice == 2:
            solution_tsp = spikes_tsp(node_indexes, nodes, speed_drone, alpha_grasp)

        # Teste com Nearest
        if tsp_choice == 3:
            solution_tsp = nearest(node_indexes, nodes, alpha_grasp)

        # print("current tsp solution = ", utils.calc_obj(solution_tsp, nodes))

        # Tratamento para retornar o depósito para início do circuito.
        for depot_index in range(len(solution_tsp)):
            if solution_tsp[depot_index] == 0:
                solution_tsp = solution_tsp[depot_index:] + \
                    solution_tsp[:depot_index]
                break

        # Construção do grafo auxiliar e das entregas por drone
        start = time.time()
        solution_tspd, operations = make_tspd_sol(
            solution_tsp, speed_truck, speed_drone, nodes)

        # print(" " + str(time.time() - start))

        # Separar as operacoes contidas em solution_tspd
        truck_nodes = solution_tspd[0]
        drone_nodes = solution_tspd[1]

        # TODO: Busca Local no TSP-D

        # Calcula custo do TSP-D
        cost_obj = calc_obj(operations, speed_truck, speed_drone, nodes)
        
        # print("current tspd solution = " + str(cost_obj))

        n_iter_w_no_improv += 1
        if cost_obj < best_cost_obj:
            best_cost_obj = cost_obj
            best_truck_nodes = list(truck_nodes)
            best_drone_nodes = list(drone_nodes)
            n_iter_w_no_improv = 0
            
        if N_ITE_GRASP == 1:
            break;    
        alpha_grasp += ALPHA_MAX/(N_ITE_GRASP - 1) 
    
    return best_cost_obj, best_truck_nodes, best_drone_nodes