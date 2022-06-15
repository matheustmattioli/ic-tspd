from cmath import inf
from tracemalloc import stop
from numpy import short
from libs.utilities import length

# TODO
# Melhorias, lista ligada para representar os grafos
# Guardar as drone deliveries em dicionarios


def subtour_cost(truck_i, truck_j, tsp_tour, speed, nodes):
    # Calcula o custo de um subtour comecando em i e terminando em j
    cost = 0
    size_tsp_tour = len(tsp_tour)
    for i in range(truck_i, truck_j):
        cost += length(nodes[tsp_tour[i]],
                       nodes[tsp_tour[(i + 1) % size_tsp_tour]])/speed
    return cost


def calc_cost(source, target, drone_node, tsp_tour, speed_truck, speed_drone, nodes, subtour_cost):
    # Computando os custos da insercao de uma entrega por drone
    dist_prevk_nextk = length(
        nodes[tsp_tour[drone_node - 1]], nodes[tsp_tour[(drone_node + 1) % len(tsp_tour)]])/speed_truck
    dist_prevk_k = length(nodes[tsp_tour[drone_node - 1]],
                          nodes[tsp_tour[drone_node]])/speed_truck
    dist_k_nextk = length(nodes[tsp_tour[drone_node]],
                          nodes[tsp_tour[(drone_node + 1) % len(tsp_tour)]])/speed_truck
    # Custo da entrega por drone
    dist_ik = length(nodes[tsp_tour[source]],
                     nodes[tsp_tour[drone_node]])/speed_drone
    dist_kj = length(nodes[tsp_tour[drone_node]],
                     nodes[tsp_tour[target % len(tsp_tour)]])/speed_drone

    return max(subtour_cost + (dist_prevk_nextk - dist_prevk_k - dist_k_nextk), dist_ik
               + dist_kj)


def make_aux_graph(tsp_tour, speed_truck, speed_drone, nodes):
    # TODO
    # Transformar o arcs em uma matriz
    arcs = []  # armazena as arestas do circuito do tsp
    drone_deliveries = []  # possiveis entregas por drone
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
            # TODO
            # Refazer o calculo do subtour_cost para conseguir eficiencia
            # constante por iteracao
            aux = subtour_cost(i, j, tsp_tour, speed_truck, nodes)
            min_value = aux
            min_index = -1
            for k in range(i + 1, j):
                # calcular custos de uma entrega por drone i -> k -> j
                cost = calc_cost(i, j, k, tsp_tour, speed_truck,
                                 speed_drone, nodes, aux)
                if cost < min_value:
                    min_value = cost
                    min_index = k
            if min_index != -1:
                if j == len(tsp_tour):
                    target = n
                else:
                    target = tsp_tour[j]
                arcs.append([tsp_tour[i], target, min_value])
                drone_deliveries.append(
                    [tsp_tour[i], tsp_tour[min_index], target, min_value])

    # TODO
    # Associar arcos com drone_deliveries atraves de um dicionario
    # print("arcs = ", arcs)
    # print("drone_deliveries = ", drone_deliveries)
    # Encontrar o caminho mais curto dentre os arcos adicionados no grafo auxiliar
    shortest_path = [-1]*(len(tsp_tour) + 1)
    cost_shortest_path = [float('inf')]*(len(tsp_tour) + 1)
    shortest_path[0] = 0
    cost_shortest_path[0] = 0
    # print("tsp_tour = ", tsp_tour)
    tsp_tour.append(n)
    
    for k in tsp_tour[1:]:
        # TODO
        # Modificar a estrutura para que o laco ande apenas nos arcos 
        # que chegam em k.
        for arc_i in arcs: 
            if k == arc_i[1] and cost_shortest_path[k] > (cost_shortest_path[arc_i[0]] + arc_i[2]):
                cost_shortest_path[k] = cost_shortest_path[arc_i[0]] + arc_i[2]
                shortest_path[k] = arc_i[0]

    # print("shortest_path = ", shortest_path)
    # print("cost_shortest_path = ", cost_shortest_path)
    return drone_deliveries, shortest_path, cost_shortest_path


def make_tspd_sol(tsp_tour, speed_truck, speed_drone, nodes):
    # Transforma as informacoes do grafo auxiliar em uma solucao tspd
    drone_deliveries, shortest_path, cost_shortest_path = make_aux_graph(
        tsp_tour, speed_truck, speed_drone, nodes)

    # Constroi o caminho armazenado em shortest_path
    j = len(tsp_tour) - 1
    # i = -1
    sol_shortest_path = []
    while j != 0:
        sol_shortest_path.append(j)
        j = shortest_path[j]
    sol_shortest_path.append(0)
    sol_shortest_path.reverse()
    
    # print("sol_shortest_path = ", sol_shortest_path)

    # Cria uma solucao para tspd apartir de sol_shortest_path
    sol_drone = []
    sol_truck = []

    # Drone Deliveries
    i = 0
    count = 0
    while i < len(sol_shortest_path) - 1:
        # Estrutura para contar quantos nós tem entre i e i+1 do
        # shortest path no tsp_tour
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
        # print("nodes_between = ", nodes_between)

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
            if found == 1:
                sol_drone.append(
                    [sol_shortest_path[i], drone_node, sol_shortest_path[i + 1]])
        i += 1
    # print("sol_drone = ", sol_drone)

    # Truck tour e operacoes

    # Operacoes servem para calcular o custo da solucao
    operations = []
    current_node = 0
    # Enquanto nao retornar ao deposito
    while current_node != len(tsp_tour) - 1:
        op_truck_nodes = []
        flag = 0
        for k_sol_drone in sol_drone:
            if current_node == k_sol_drone[0]:
                # print("current_node = ", current_node)
                for i in range(len(tsp_tour)):
                    if tsp_tour[i] == current_node:
                        start_append = i
                    elif tsp_tour[i] == k_sol_drone[2]:
                        end_append = i
                for i in range(start_append, end_append):
                    if tsp_tour[i] != k_sol_drone[1]:
                        sol_truck.append(tsp_tour[i])
                for i in range(start_append, end_append + 1):
                    if tsp_tour[i] != k_sol_drone[1]:
                        op_truck_nodes.append(tsp_tour[i])
                current_node = k_sol_drone[2]
                op_drone_nodes = [k_sol_drone[0], k_sol_drone[1], k_sol_drone[2]]
                if k_sol_drone[2] == tsp_tour[-1]:
                    op_drone_nodes = [k_sol_drone[0], k_sol_drone[1], 0]
                if op_truck_nodes[-1] == tsp_tour[-1]:
                    op_truck_nodes[-1] = 0
                # print([op_truck_nodes, op_drone_nodes])
                operations.append([op_truck_nodes, op_drone_nodes])
                op_truck_nodes = []
                flag = 1
        if flag == 0:
            sol_truck.append(current_node)
            op_truck_nodes.append(current_node)
            for i in range(len(tsp_tour)):
                if tsp_tour[i] == current_node:
                    current_node = tsp_tour[(i + 1) % len(tsp_tour)]
                    break
            op_truck_nodes.append(current_node)
            if op_truck_nodes[-1] == tsp_tour[-1]:
                op_truck_nodes[-1] = 0
            op_drone_nodes = []
            # print([op_truck_nodes, op_drone_nodes])
            operations.append([op_truck_nodes, op_drone_nodes])
    tspd_sol = [sol_truck, sol_drone]
    return tspd_sol, operations
