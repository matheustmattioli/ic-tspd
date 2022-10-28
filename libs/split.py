from platform import node
import numpy as np
from libs.utilities import length


# Calcula o custo de um subtour comecando em i e terminando em j
def subtour_cost(truck_i, truck_j, tsp_tour, speed, nodes):
    cost = 0
    size_tsp_tour = len(tsp_tour)
    for i in range(truck_i, truck_j):
        cost += length(nodes[tsp_tour[i]],
                       nodes[tsp_tour[(i + 1) % size_tsp_tour]])/speed
    return cost

# Função para procurar elemento em lista
def search(list, target):
    for i in range(len(list)):
        if list[i] == target:
            return i
    return -1

# Função para deixar a lista de arrays em uma lista comum
def flatten_list(_2d_list):
    flat_list = []
    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

# Calculo da função objetivo
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

# TODO:
def lazy_drone():
    pass

# O drone é "preguiçoso", ele não gastar muito tempo
# em sua entrega i -> k -> j, só valores menores ou 
# iguais ao tempo empregado pelo caminhão 
# no percurso i -> j. Em outras palavras, o caminhão
# não pode parar de rodar.
# Recebe: 
#   . um circuito que resolve um TSP;
#   . velocidade do caminhão;
#   . velocidade do drone;
#   . os nós do grafo;
def make_aux_graph_simple_lazy(tsp_tour, speed_truck, speed_drone, nodes):

    # Matriz de adjacência. 
    # Eficiência de O(n²) para operações de busca, 
    # além de ocupar bastante espaço na memória
    arcs = np.full((len(tsp_tour) + 1, len(tsp_tour) + 1), np.inf)

    drone_deliveries = dict()  # possiveis entregas por drone

    # Início construção do grafo auxiliar.
    # Inserção das arestas do TSP em arcs,
    # a matriz arcs é indexada pelos rótulos dos vértices do grafo.
    n = len(tsp_tour)
    for i in range(n - 1):
        node_i = tsp_tour[i]
        node_j = tsp_tour[i + 1]
        arcs[node_i, node_j] = length(nodes[node_i], nodes[node_j])/speed_truck
    # Arco do final pro começo para o nó artificial (réplica do depósito).
    arcs[
        tsp_tour[n - 1],
        n
        ] = length(nodes[tsp_tour[n - 1]], nodes[0])/speed_truck
    
    # Implementando versão simplificada, aquela em que
    # escolhemos um nó do *caminho* para ser i (lançamento) 
    # e outro para ser k (entrega do drone), daí os destinos são os vértices
    # maiores que k até encontrarmos o primeiro vértice j
    # com valor dist_caminhão(i -> j) >= dist_drone(i -> k -> j)
    for i in range(n - 1): # 0, 1, ..., n - 2
        # Para calcular a distância do caminhão entre i, j
        # precisamos calcular a distância percorrida pelo caminhão a cada incremento de k
        # para buscarmos a eficiência O(n²) no caso médio, que é o grande propósito dessa
        # implementação.
        dist_truck_ik = 0 # distância percorrida pelo caminhão seguindo a rota de i até k
        for k in range(i + 1, n): # i + 1, i + 2, ..., n - 1
            # Distâncias para cálculo da propriedade lazy
            # Cálculo do caminho do caminhão
            # no começo, i = k - 1
            dist_truck_ik += length(
                nodes[tsp_tour[k - 1]], nodes[tsp_tour[k]])/speed_truck

            # Cálculo da ida do drone
            dist_drone_ik = length(nodes[tsp_tour[i]],
                     nodes[tsp_tour[k]])/speed_drone

            # Cálculo do "triângulo" do drone node
            truck_triang = (length(nodes[tsp_tour[k - 1]], nodes[tsp_tour[(k + 1) % len(tsp_tour)]])/speed_truck) \
                - (length(nodes[tsp_tour[k - 1]], nodes[tsp_tour[k]])/speed_truck 
                   + length(nodes[tsp_tour[k]], nodes[tsp_tour[(k + 1) % len(tsp_tour)]])/speed_truck
                )

            # distância percorrida pelo caminhão seguindo a rota de k até j
            dist_truck_kj = 0 

            for j in range(k + 1, n + 1):
                # Cálculo da volta do drone
                dist_drone_kj = length(nodes[tsp_tour[k]],
                        nodes[tsp_tour[j % n]])/speed_drone
                # Cálculo caminho caminhão até j
                dist_truck_kj += length(nodes[tsp_tour[j - 1]], nodes[tsp_tour[j % n]])/speed_truck

                # Cálculo da rota do caminhão sem o "triângulo" do drone node
                dist_truck = dist_truck_ik + dist_truck_kj + truck_triang 
                # distância percorrida pelo drone, para realizar a entrega
                dist_drone = dist_drone_ik + dist_drone_kj

                candidate_cost = max(dist_truck, dist_drone)
                if j != n:
                    target = tsp_tour[j]
                else:
                    target = n
                previous_cost = arcs[tsp_tour[i], target]

                if candidate_cost < previous_cost:
                    arcs[tsp_tour[i], target] = candidate_cost
                    drone_deliveries[(tsp_tour[i], target)] = tsp_tour[k]
                        
                if dist_truck >= dist_drone:
                    break
     
    # print(arcs)
    # print("drone_deliveries = ", drone_deliveries)

    # Encontrar o caminho mais curto dentre os arcos adicionados no grafo auxiliar
    pred_shortest_path = np.full(n + 1, -1)
    cost_shortest_path = np.full(n + 1, np.inf)
    pred_shortest_path[0] = 0
    cost_shortest_path[0] = 0
    tsp_tour.append(n)

    # Buscando apenas arcos de chegada, utilizar a matriz de adjacencia para melhorar o desempenho dessa parte
    for j in range(1, n + 1):
        for i in range(0, j):
            cost = arcs[tsp_tour[i], tsp_tour[j]]
            if cost_shortest_path[tsp_tour[j]] > (cost_shortest_path[tsp_tour[i]] + cost):
                cost_shortest_path[tsp_tour[j]] = cost_shortest_path[tsp_tour[i]] + cost
                pred_shortest_path[tsp_tour[j]] = tsp_tour[i]

    tsp_tour.pop()
    # print("shortest_path = ", shortest_path)
    # print("cost_shortest_path = ", cost_shortest_path)
    return drone_deliveries, pred_shortest_path, cost_shortest_path

def make_aux_graph(tsp_tour, speed_truck, speed_drone, nodes):

    # armazena as arestas do circuito do tsp
    arcs = np.full((len(tsp_tour) + 1, len(tsp_tour) + 1), np.inf)

    drone_deliveries = dict()  # possiveis entregas por drone

    # Construcao do grafo auxiliar
    # Inserir as arestas do TSP em arcs
    # TODO:
    # Matriz de adjacência com muitos 0, tem como melhorar
    # utilizando listas ligadas
    # pesquisar como usar listas ligadas em python

    # matriz arcs indexados pelos rótulos dos vértices.
    n = len(tsp_tour)
    for i in range(n - 1):
        node_i = tsp_tour[i]
        node_j = tsp_tour[i + 1]
        arcs[node_i, node_j] = length(nodes[node_i], nodes[node_j])/speed_truck
    # arco do final pro começo
    arcs[tsp_tour[n - 1],
         n] = length(nodes[tsp_tour[n - 1]], nodes[0])/speed_truck

    # Computar possiveis entregas por drone
    for i in range(n - 1):
        for j in range(i + 2, n + 1):
            # Da para diminuir a constante desses laços
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
                arcs[tsp_tour[i], target] = min_value
                drone_deliveries[(tsp_tour[i], target)] = tsp_tour[min_index]

    # print(arcs)
    # print("drone_deliveries = ", drone_deliveries)

    
    # Encontrar o caminho mais curto dentre os arcos adicionados no grafo auxiliar
    pred_shortest_path = np.full(n + 1, -1)
    cost_shortest_path = np.full(n + 1, np.inf)
    pred_shortest_path[0] = 0
    cost_shortest_path[0] = 0
    tsp_tour.append(n)

    # Buscando apenas arcos de chegada, utilizar a matriz de adjacencia para melhorar o desempenho dessa parte
    for j in range(1, n + 1):
        for i in range(0, j):
            cost = arcs[tsp_tour[i], tsp_tour[j]]
            if cost_shortest_path[tsp_tour[j]] > (cost_shortest_path[tsp_tour[i]] + cost):
                cost_shortest_path[tsp_tour[j]] = cost_shortest_path[tsp_tour[i]] + cost
                pred_shortest_path[tsp_tour[j]] = tsp_tour[i]

    tsp_tour.pop()
    # print("shortest_path = ", shortest_path)
    # print("cost_shortest_path = ", cost_shortest_path)
    return drone_deliveries, pred_shortest_path, cost_shortest_path


def make_tspd_sol(tsp_tour, speed_truck, speed_drone, nodes):
    # Transforma as informacoes do grafo auxiliar em uma solucao tspd

    # drone_deliveries, path_pred, cost_shortest_path = make_aux_graph(
    #     tsp_tour, speed_truck, speed_drone, nodes)

    drone_deliveries, path_pred, cost_shortest_path = make_aux_graph_simple_lazy(
        tsp_tour, speed_truck, speed_drone, nodes)

    # Constroi o caminho armazenado em shortest_path
    j = len(tsp_tour)
    shortest_path = []
    while j != 0:
        shortest_path.append(j)
        j = path_pred[j]
    shortest_path.append(0)
    shortest_path.reverse()

    # print("shortest_path = ", shortest_path)
    # print("tsp_tour = ", tsp_tour)
    # print("drone_deliveries = ", drone_deliveries)

    # Cria uma solucao para tspd apartir de sol_shortest_path
    sol_drone = []
    sol_truck = []
    # Armazena em modo de operacoes, para calculo da funcao objetivo
    operations = []

    # Entregas por drone e caminhão
    tam_solsp = len(shortest_path)
    n = len(tsp_tour)
    i = 0
    i_launch = 0
    
    while i < tam_solsp - 1:
        # Encontrar a entrega por drone associada a esse par de vértices
        launch = shortest_path[i]
        rendezvous = shortest_path[i + 1]
        # Verifica se tem um drone associado
        # Se não tiver, então é um trecho com o drone junto do caminhão
        drone = -1
        if (launch, rendezvous) in drone_deliveries.keys():
            drone = drone_deliveries[launch, rendezvous]
            drone_tour = [launch, drone, rendezvous]
            if drone_tour[-1] == n:
                drone_tour[-1] = 0
            # k = search(drone_tour, n - 1)
            # if k != -1:
            #     drone_tour[k] = 0
        else:
            drone_tour = []
        sol_drone.append(drone_tour)
        # Pegar o tour do caminhão associado a essa entrega por drone
        # vai do nó launch até o rendezvous.
        truck_tour = [launch]
        # Encontrar posição do nó launch no tsp_tour
        # orig armazena a posição do vértice de lançamento
        # rend armazena a posição do vértice de encontro
        i_rendezvous = i_launch + 1
        while i_rendezvous < n and tsp_tour[i_rendezvous] != rendezvous:
            if tsp_tour[i_rendezvous] != drone:
                truck_tour.append(tsp_tour[i_rendezvous])
            i_rendezvous += 1
        truck_tour.append(rendezvous)

        # formatar a saída para formato utilizado até então
        # transformar todo nó tam_instancia em 0.
        # no caso dessa funçao tam_instancia = n - 1, pois tsp_tour já conta com
        # esse nó duplicado
        # a do truck_tour ta implementado aqui e o do drone_tour na linha 145 ~ 147
        if truck_tour[-1] == n:
            truck_tour[-1] = 0
        # k = search(truck_tour, n - 1)
        # if k != -1:
        #     truck_tour[k] = 0

        sol_truck.append(truck_tour)
        operations.append([truck_tour, drone_tour])
        i += 1
        i_launch = i_rendezvous

    # print("sol_truck = ", sol_truck)
    # print("sol_drone = ", sol_drone)

    sol_truck = flatten_list(sol_truck)
    sol_truck = list(dict.fromkeys(sol_truck))

    tspd_sol = [sol_truck, sol_drone]
    return tspd_sol, operations
