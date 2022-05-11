# Script para calcular distâncias entre nós das instâncias
import math

coord_x = [0.15828775484363333, 71.0, 88.0, 16.0, 58.0, 61.0, 3.0, 73.0, 21.0]
coord_y = [0.04446745491602355, 82.0, 66.0, 67.0, 82.0, 0.0, 80.0, 91.0, 1.0]

def length(node1, node2, coord_x, coord_y):
    # Função que calcula distância euclidiana entre dois vértices do plano.

    return math.sqrt((coord_x[node1] - coord_x[node2])**2 + (coord_y[node1] - coord_y[node2])**2)

for i in range(len(coord_x)):
    for j in range(len(coord_x)):
        print("dist ",i, j, '%.2f' % length(i, j, coord_x, coord_y), '%.2f' % (length(i, j, coord_x, coord_y)/3))