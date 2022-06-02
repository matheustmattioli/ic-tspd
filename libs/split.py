from cmath import inf
from tracemalloc import stop
from numpy import short
from libs.calc_dist import length

def subtour_cost(truck_i, truck_j, tsp_tour, speed):
    # Calcula o custo de um subtour comecando em i e terminando em j
    cost = 0
    for i in range(truck_j - truck_i):
        cost += length(tsp_tour[truck_i + i], tsp_tour[truck_i + i + 1])/speed 
    return cost

def calc_cost(truck_i, truck_j, drone_k, tsp_tour, speed_truck, speed_drone):
    # Computando os custos da insercao de uma entrega por drone
    sub_cost = subtour_cost(truck_i, truck_j, tsp_tour, speed_truck)
    dist_prevk_nextk = length(tsp_tour[drone_k - 1], tsp_tour[drone_k + 1])/speed_truck
    dist_prevk_k = length(tsp_tour[drone_k - 1], tsp_tour[drone_k])/speed_truck
    dist_k_nextk = length(tsp_tour[drone_k], tsp_tour[drone_k + 1])/speed_truck
    # Custo da entrega por drone
    dist_ik = length(tsp_tour[truck_i], tsp_tour[drone_k])/speed_drone
    dist_kj = length(tsp_tour[drone_k], tsp_tour[truck_j])/speed_drone
    # Tempo de espera
    wait_time_truck = max(0, sub_cost - (dist_ik + dist_kj))
    wait_time_drone = max(0, (dist_ik + dist_kj) - sub_cost)

    return sub_cost + (dist_prevk_nextk - dist_prevk_k - dist_k_nextk) + dist_ik \
        + dist_kj + wait_time_drone + wait_time_truck

def make_aux_graph(tsp_tour, speed_truck, speed_drone):
    arcs = []  # armazena as arestas do circuito do tsp
    drone_deliveries = [] # possiveis entregas por drone
    # Construcao do grafo auxiliar
    # Inserir as arestas do tsp em arcs
    for i in range(len(tsp_tour) - 1):
        arcs.append([tsp_tour[i], tsp_tour[i + 1], length(tsp_tour[i], tsp_tour[i + 1])]/speed_truck)
    # Computar possiveis entregas por drone
    for i in range(len(tsp_tour) - 2):
        for j in range(len(tsp_tour) - 1):
            min_value = float('inf')
            min_index = float('inf')
            for k in range(len(tsp_tour)):
                if i < k and k < j:
                    # calcular custos de uma entrega por drone i -> k -> j
                    cost = calc_cost(i, j, k, tsp_tour, speed_truck, speed_drone) 
                    if cost < min_value:
                        min_value = cost
                        min_index = k
            arcs.append([tsp_tour[i], tsp_tour[j], min_value])
            drone_deliveries.append([tsp_tour[i], tsp_tour[min_index], tsp_tour[j], min_value])

    # Encontrar o caminho mais curto
    shortest_path = [float('inf')]*len(tsp_tour)
    cost_shortest_path = [float('inf')]*len(tsp_tour)
    shortest_path[0] = 0
    cost_shortest_path[0] = 0

    for k in tsp_tour:
        if k != 0:
            for arc_i in arcs:
                if k == arc_i[1] and cost_shortest_path[k] > (cost_shortest_path[arc_i[0]] + arc_i[2]):
                    cost_shortest_path[k] = cost_shortest_path[arc_i[0]] + arc_i[2]
                    shortest_path[k] = arc_i[0]


    return drone_deliveries, shortest_path, cost_shortest_path

def make_tspd_sol(tsp_tour, speed_truck, speed_drone):
    # Transforma as informacoes do grafo auxiliar em uma solucao tspd
    drone_deliveries, shortest_path, cost_shortest_path = make_aux_graph(tsp_tour, speed_truck, speed_drone)

    # Constroi o caminho armazenado em shortest_path
    j = len(tsp_tour)
    i = float('inf')
    sol_shortest_path = [j]
    while i != 0:
        i = shortest_path[j]
        sol_shortest_path.append(i)
        j = i
    sol_shortest_path.reverse()

    # Cria uma solucao para tspd apartir de sol_shortest_path
    sol_drone = []
    sol_truck = []

    # Drone Deliveries
    i = 0
    while i < len(sol_shortest_path):
        nodes_between = tsp_tour[sol_shortest_path[i]] - tsp_tour[sol_shortest_path[i + 1]]
        if nodes_between != 0:
            # pegar o vertice atendido pelo drone associado aos nos i e i + 1
            for k_drone in drone_deliveries:
                if k_drone[0] == sol_shortest_path[i] and k_drone[2] == sol_shortest_path[i + 1]:
                    drone_node = k_drone[1]
            sol_drone.append[sol_shortest_path[i], drone_node, sol_shortest_path[i + 1]]
        i += 1
    # Truck tour
    current_node = 0
    while current_node != len(tsp_tour):       
        flag = 0
        for k_sol_drone in sol_drone:
            if current_node == k_sol_drone[0]:
                
                current_node = k_sol_drone[2]
                flag = 1
        if flag == 0:
            sol_truck.append(current_node)
            for i in range(len(tsp_tour)):
                if tsp_tour[i] == current_node:
                    current_node = tsp_tour[i + 1]
                    break
            
    tspd_sol = [sol_truck, sol_drone]
    return tspd_sol
