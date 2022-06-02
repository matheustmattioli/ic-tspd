from cmath import inf
from tracemalloc import stop
from numpy import short
from libs.utilities import length

def subtour_cost(truck_i, truck_j, tsp_tour, speed, nodes):
    # Calcula o custo de um subtour comecando em i e terminando em j
    cost = 0
    for i in range(truck_i, truck_j):
        cost += length(nodes[tsp_tour[i]], nodes[tsp_tour[i + 1]])/speed 
    return cost

def calc_cost(source, target, drone, tsp_tour, speed_truck, speed_drone, nodes, sub_cost):
    # Computando os custos da insercao de uma entrega por drone
    dist_prevk_nextk = length(nodes[tsp_tour[drone - 1]], nodes[tsp_tour[drone + 1]])/speed_truck
    dist_prevk_k = length(nodes[tsp_tour[drone - 1]], nodes[tsp_tour[drone]])/speed_truck
    dist_k_nextk = length(nodes[tsp_tour[drone]], nodes[tsp_tour[drone + 1]])/speed_truck
    # Custo da entrega por drone
    dist_ik = length(nodes[tsp_tour[source]], nodes[tsp_tour[drone]])/speed_drone
    dist_kj = length(nodes[tsp_tour[drone]], nodes[tsp_tour[target]])/speed_drone
    
    return max(sub_cost + (dist_prevk_nextk - dist_prevk_k - dist_k_nextk), dist_ik \
        + dist_kj)

def make_aux_graph(tsp_tour, speed_truck, speed_drone, nodes):
    arcs = []  # armazena as arestas do circuito do tsp
    drone_deliveries = [] # possiveis entregas por drone
    # Construcao do grafo auxiliar
    # Inserir as arestas do tsp em arcs
    for i in range(len(tsp_tour) - 1):
        arcs.append([tsp_tour[i], tsp_tour[(i + 1)], 
            length(nodes[tsp_tour[i]], nodes[tsp_tour[(i + 1)]])/speed_truck])
    n = len(tsp_tour)
    arcs.append([tsp_tour[n - 1], n,
        length(nodes[tsp_tour[n - 1]], nodes[0])/speed_truck])
    # Computar possiveis entregas por drone
    for i in range(len(tsp_tour)):
        for j in range(i + 2, len(tsp_tour) + 1):
            aux = subtour_cost(i, j, tsp_tour, speed_truck, nodes)
            min_value = aux
            min_index = -1
            for k in range(i + 1, j):
                # print("entrou")
                # print(i, k, j)
                # calcular custos de uma entrega por drone i -> k -> j
                cost = calc_cost(i, j, k, tsp_tour, speed_truck, speed_drone, nodes, aux) 
                if cost < min_value:
                    min_value = cost
                    min_index = k
            # print(i)
            # print(min_index)
            # print(j)
            if min_index != -1:
                arcs.append([tsp_tour[i], tsp_tour[j], min_value])
                drone_deliveries.append([tsp_tour[i], tsp_tour[min_index], tsp_tour[j], min_value])

    # Encontrar o caminho mais curto
    print("arcs = ", arcs)
    shortest_path = [float('inf')]*len(tsp_tour)
    cost_shortest_path = [float('inf')]*len(tsp_tour)
    shortest_path[0] = 0
    cost_shortest_path[0] = 0
    print("tsp_tour = ", tsp_tour)
    for k in tsp_tour:
        if k != 0:
            for arc_i in arcs:
                if k == arc_i[1] and cost_shortest_path[k] > (cost_shortest_path[arc_i[0]] + arc_i[2]):
                    cost_shortest_path[k] = cost_shortest_path[arc_i[0]] + arc_i[2]
                    shortest_path[k] = arc_i[0]

    print("shortest_path = ", shortest_path)
    print("cost_shortest_path = ", cost_shortest_path)
    print("drone_deliveries = ", drone_deliveries)
    return drone_deliveries, shortest_path, cost_shortest_path

def make_tspd_sol(tsp_tour, speed_truck, speed_drone, nodes):
    # Transforma as informacoes do grafo auxiliar em uma solucao tspd
    drone_deliveries, shortest_path, cost_shortest_path = make_aux_graph(tsp_tour, speed_truck, speed_drone, nodes)

    # Constroi o caminho armazenado em shortest_path
    j = len(tsp_tour) - 1 
    i = float('inf')
    sol_shortest_path = [j]
    while i != 0:
        i = shortest_path[j]
        sol_shortest_path.append(i)
        j = i
    sol_shortest_path.reverse()

    print("sol_shortest_path = ", sol_shortest_path)
    # Cria uma solucao para tspd apartir de sol_shortest_path
    sol_drone = []
    sol_truck = []

    # Drone Deliveries
    i = 0
    count = 0
    while i < len(sol_shortest_path) - 1:
        for m in range(len(tsp_tour)):
            if tsp_tour[m] == sol_shortest_path[i]:
                break
        for n in range(len(tsp_tour)):
            if tsp_tour[n] == sol_shortest_path[i + 1]:
                break
        for h in range(len(tsp_tour)):
            if tsp_tour[h] == tsp_tour[m]:
                for l in range(h + 1, len(tsp_tour)):
                    if tsp_tour[l] == tsp_tour[n]:
                        break
                    count += 1
                break
        nodes_between = count
        count = 0
        print("nodes_between = ", nodes_between)
        
        found = 0
        if nodes_between > 0:
            # pegar o vertice atendido pelo drone associado aos nos i e i + 1
            for k_drone in drone_deliveries:
                # print("k_drone = ", k_drone)
                # print("k_drone[0] = ", k_drone[0])
                # print("sol_shortest_path[i] = ", sol_shortest_path[i])
                # print("k_drone[2] = ", k_drone[2])
                # print("sol_shortest_path[i + 1] = ", sol_shortest_path[i + 1])
                if k_drone[0] == sol_shortest_path[i] and k_drone[2] == sol_shortest_path[i + 1]:
                    drone_node = k_drone[1]
                    found = 1
                    print("entrou🤔")
            if found == 1:
                sol_drone.append([sol_shortest_path[i], drone_node, sol_shortest_path[i + 1]])
        i += 1
    print("sol_drone = ", sol_drone)
    # Truck tour
    current_node = 0
    while current_node != len(tsp_tour):       
        flag = 0
        for k_sol_drone in sol_drone:
            if current_node == k_sol_drone[0]:
                for i in range(len(tsp_tour)):
                    if tsp_tour[i] == current_node:
                        start_append = i
                    elif tsp_tour[i] == k_sol_drone[2]:
                        end_append = i
                for i in range(start_append, end_append + 1):
                    if tsp_tour[i] != k_sol_drone[1]:
                        sol_truck.append(tsp_tour[i])
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
