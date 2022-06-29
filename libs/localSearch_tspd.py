import libs.utilities as utilities



def localSearch2OPT_truck(cluster, customers):
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