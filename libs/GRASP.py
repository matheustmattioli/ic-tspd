import libs.greedyRCL as greedyRCL
import libs.localSearch as localSearch

ALPHA_MAX = 0.5
N_ITE_GRASP = 500 # Number of iterations GRASP.
MAX_ITER_W_NO_IMPROV = 100

def grasp_vnd(cluster_vehicle, customers):
    # Greedy Randomized Adaptative Search Procedure (GRASP) implementation with 
    # Local Search 2-OPT as "Search Procedure". 
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