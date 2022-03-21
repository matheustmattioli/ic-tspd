import libs.utilities as utilities



def localSearch2OPT(cluster, customers):
    # Local Search for TSP with 2OPT neighbour structure.
    # Small improvements in solutions through analyze of neighborhoods
    obj = utilities.calc_obj(cluster, customers) # Cost of the initial solution
    customer_count = len(cluster)
    # Initialize variables with datas from the initial solution
    lenght_BS = obj 
    lenght_solution = lenght_BS
    best_solution = list(cluster)
    # Main loop
    while True: 
        try:
            lenght_BF = lenght_solution
            best_x = customer_count - 1
            best_y = 0
            # 2-OPT NEIGHBORHOOD
            for x in range(0, customer_count - 2):
                for y in range(x + 1, customer_count - 1):
                    edgeA = utilities.length(customers[cluster[x]], \
                        customers[cluster[x - 1]])
                    edgeB = utilities.length(customers[cluster[y]], \
                        customers[cluster[(y + 1) % customer_count]])
                    edgeC = utilities.length(customers[cluster[x]], \
                        customers[cluster[(y + 1) % customer_count]])
                    edgeD = utilities.length(customers[cluster[y]], \
                        customers[cluster[(x - 1)]])
                    lenght_PS = lenght_solution - (edgeA + edgeB) 
                    lenght_PS = lenght_PS + (edgeC + edgeD)
                    if lenght_PS < lenght_BF:
                        best_x = x
                        best_y = y
                        lenght_BF = lenght_PS
            cluster[best_x:best_y + 1] =  cluster[best_x:best_y + 1][::-1]
            lenght_solution = lenght_BF
            # Update solution
            if lenght_solution < lenght_BS:
                best_solution = list(cluster)
                lenght_BS = lenght_solution
            else:
                break                
        except KeyboardInterrupt:
            break
    return best_solution, lenght_BS

def localSearch3OPT(cluster, customers):
    # Local Search for TSP with 3OPT neighbour structure.
    # Small improvements in solutions through analyze of neighborhoods
    node_count = len(cluster)
    obj = utilities.calc_obj(cluster, customers) # Cost of the initial solution
    # Initialize variables with datas from the initial solution
    length_BS = obj 
    length_solution = length_BS
    best_solution = list(cluster) 
    # Main loop
    while True: 
        try:
            length_BF = length_solution
            combination = 0
            best_combination = 0
            best_x = node_count - 1
            best_z = node_count - 1
            best_y = 0
            # 3-OPT NEIGHBORHOOD
            for x in range(0, node_count - 3):
                for y in range(x + 1, node_count - 2):
                    for z in range(y + 1, node_count - 1):
                        # cut 3 edges
                        edgeA = utilities.length(customers[cluster[x]],
                                    customers[cluster[x + 1]])
                        edgeB = utilities.length(customers[cluster[y]],
                                    customers[cluster[y + 1]])
                        edgeC = utilities.length(
                            customers[cluster[z]], customers[cluster[(z + 1) % node_count]])
                        """ 3 arestas inseridas
                        testar as 3 combinacoes de arestas """
                        # Combination I
                        edgeD = utilities.length(customers[cluster[x]],
                                    customers[cluster[y + 1]])
                        edgeE = utilities.length(customers[cluster[z]],
                                    customers[cluster[y]])
                        edgeF = utilities.length(
                            customers[cluster[x + 1]], customers[cluster[(z + 1) % node_count]])
                        # Combination II
                        edgeG = utilities.length(customers[cluster[x]],
                                    customers[cluster[y]])
                        edgeH = utilities.length(
                            customers[cluster[x + 1]], customers[cluster[z]])
                        edgeI = utilities.length(
                            customers[cluster[y + 1]], customers[cluster[(z + 1) % node_count]])
                        # Combination III
                        edgeJ = utilities.length(customers[cluster[x]],
                                    customers[cluster[z]])
                        edgeK = utilities.length(
                            customers[cluster[y + 1]], customers[cluster[x + 1]])
                        edgeL = utilities.length(
                            customers[cluster[y]], customers[cluster[(z + 1) % node_count]])
                        # Combination IV
                        edgeM = utilities.length(customers[cluster[x]],
                                    customers[cluster[y + 1]])
                        edgeN = utilities.length(customers[cluster[z]],
                                    customers[cluster[x + 1]])
                        edgeO = utilities.length(customers[cluster[y]],
                                       customers[cluster[(z + 1) % node_count]])
                        """ Select best edges """
                        cost_decrease = edgeA + edgeB + edgeC
                        cost_increase1 = edgeD + edgeE + edgeF
                        cost_increase2 = edgeG + edgeH + edgeI
                        cost_increase3 = edgeJ + edgeK + edgeL
                        cost_increase4 = edgeM + edgeN + edgeO
                        if cost_increase1 <= cost_increase2:
                            cost_increase = cost_increase1
                            combination = 1
                        else:
                            cost_increase = cost_increase2
                            combination = 2
                        if cost_increase3 < cost_increase:
                            cost_increase = cost_increase3
                            combination = 3
                        if cost_increase4 < cost_increase:
                            cost_increase = cost_increase4
                            combination = 4
                        length_PS = length_solution - cost_decrease + cost_increase
                        if length_PS < length_BF:
                            best_x = x
                            best_y = y
                            best_z = z
                            length_BF = length_PS
                            best_combination = combination
            # Forming new circuit
            if best_combination == 1:   
                cluster = list(cluster[:best_x + 1] + cluster[best_y + 1:best_z + 1] \
                    + cluster[best_y:best_x: -1] + cluster[best_z + 1:])
            elif best_combination == 2:
                cluster = list(cluster[:best_x + 1] + cluster[best_y:best_x: -1] + \
                    cluster[best_z:best_y: -1] + cluster[best_z + 1:])
            elif best_combination == 3:
                cluster = list(cluster[:best_x + 1] + cluster[best_z:best_y: -1] + \
                    cluster[best_x + 1:best_y + 1] + cluster[best_z + 1:])
            elif best_combination == 4:
                cluster = list(cluster[:best_x + 1] + cluster[best_y + 1:best_z + 1] + \
                    cluster[best_x + 1:best_y + 1] + cluster[best_z + 1:])
            length_solution = length_BF
            # Update solution
            if length_solution < length_BS:
                best_solution = list(cluster)
                length_BS = length_solution
            else:
                break
        except KeyboardInterrupt:
            break
    return best_solution, length_BS

def localSearchVNS(circuit, customers):
    # Variable Neighbourhood Search (VNS)
    # Change between 2-OPT and 3-OPT neighbour structure when find local minima, 
    # until there is no way to improvement. 
    best_obj = utilities.calc_obj(circuit, customers) # calc cost of initial solution
    best_circuit = list(circuit)
    while True:
        try:
            circuit, obj = localSearch2OPT(best_circuit, customers)
            if obj < best_obj:
                best_obj = obj
                best_circuit = list(circuit)
            else:
                circuit, obj = localSearch3OPT(best_circuit, customers)
                if obj < best_obj:
                    best_obj = obj
                    best_circuit = list(circuit)
                else:
                    break
        except:
            break
    return best_circuit, best_obj