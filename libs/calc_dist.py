# Script para calcular distâncias entre nós das instâncias
import math

coord_x = [31.72211530938005, -40.13758014155382, 199.1940477020881, 0.050486787470969956, 211.52327482026735]
coord_y = [-20.383734992809732, -8.209018925046815, 4.752478364864648, 25.263512891082936, 1.2483288702191122]

def length(node1, node2, coord_x, coord_y):
    # Função que calcula distância euclidiana entre dois vértices do plano.

    return math.sqrt((coord_x[node1] - coord_x[node2])**2 + (coord_y[node1] - coord_y[node2])**2)

for i in range(len(coord_x)):
    for j in range(len(coord_x)):
        print("dist ",i, j, '%.2f' % length(i, j, coord_x, coord_y), '%.2f' % (length(i, j, coord_x, coord_y)/2))