import math     # Para cálculo de distâncias no plano euclidiano

def length(node1, node2):
    # Função que calcula distância euclidiana entre dois vértices do plano.
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

def calc_obj(tour, nodes):
    cost_obj = 0
    for i in range(len(tour)):
        cost_obj += length(nodes[tour[i - 1]], nodes[tour[i]])
    return cost_obj