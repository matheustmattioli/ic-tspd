from adapter.adapt_tspd_author import calc_obj
import libs.greedyRCL as greedyRCL
import libs.localSearch as localSearch
import random
from libs.split import make_tspd_sol


random.seed(4542355562136458828)

def nearest_vnd(cluster_vehicle, customers):
    
    solution_vehicle, _ = greedyRCL.greedypath_RCL(cluster_vehicle, customers, 0)
    solution_vehicle, _ = localSearch.localSearchVNS(solution_vehicle, customers)

    return solution_vehicle

def solve_tspd_nearest_vnd(nodes, speed_truck, speed_drone):

    # Array de rótulos dos nós.
    node_indexes = []
    for node in nodes:
        node_indexes.append(node.index)

    
    # Nearest-VND para formar TSP
    solution_tsp = nearest_vnd(node_indexes, nodes)

    # Tratamento para retornar o depósito para início do circuito.
    for depot_index in range(len(solution_tsp)):
        if solution_tsp[depot_index] == 0:
            solution_tsp = solution_tsp[depot_index:] + \
                solution_tsp[:depot_index]
            break
    
    solution_tspd, operations = make_tspd_sol(solution_tsp, speed_truck, speed_drone, nodes)

    # Separar as operacoes contidas em solution_tspd
    truck_nodes = solution_tspd[0]
    drone_nodes = solution_tspd[1]

    cost_obj = calc_obj(operations, speed_truck, speed_drone, nodes)

    return cost_obj, truck_nodes, drone_nodes
            
