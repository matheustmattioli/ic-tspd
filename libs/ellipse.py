
# Heurística construtiva para TSP.
# Comportamento Guloso-Aleatorizado.
def ellipse(array_nodes, customers):

    # Formar um circuito com vértices interessantes para entregas por drone,
    # para isso vamos selecionar vértices em uma vizinhança em formato de elipse 
    # para serem colocadas na Lista Restrita de Candidatos (RCL)
    # Essa vizinhança é definida pela equação second_nearest + (furthest - second_nearest)*ALPHA*DELTA
    # Sendo que o ALPHA é a constante que define uma porcentagem dos valores furthest e secon_nearest
    # para ser considerado.
    # DELTA é um valor a ser calculado com base ???
    size_circuit = len(array_nodes)
    dict_nodes = {array_nodes[i] : array_nodes[i] for i in range(size_circuit)}
    solution_ellipse = [0 for i in range(size_circuit)]
