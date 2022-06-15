# Neste script python vamos formar um csv das soluções obtidas 
# armazenadas nos arquivos do caminho:
# .\data\solutions\

# Vamos formar um csv no formato:
# Nome Instancia, Solucao otima TSP, Solucao GRASP TSP, Tempo GRASP TSP e Solucao TSPD
import csv
from pickle import GLOBAL
import sys
import os
from progress.bar import Bar 



def make_data_csv(input_data, file_name):
    # read data
    # print(input_data)
    tspd_value = input_data[0].split('\n')
    auth_data = input_data[1].split('\n')
    our_data = input_data[2].split('\n')

    # coleta info desejada
    auth_value = float(auth_data[0])
    our_value = float(our_data[0])
    
    our_time = str(our_data[1]).strip()
    tspd_value = str(tspd_value[0]).strip()

    # tratamento file_name
    file_name = file_name.split("\\")[-1]
    file_name = file_name.split(".sol")[0]
    return [file_name, auth_value, our_value, our_time, tspd_value]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        start = 'yes'
        first_it = 1
        while start == 'yes':
            count = 0
            if first_it == 1:
                path = sys.argv[1].strip()
                first_it = 0
            else:
                path = input("Digite o endereco do diretorio:")
            # EXEMPLOS:
            # path = ".\\data\\solutions\\doublecenter"
            # path = ".\\data\\solutions\\filtered_data\\pequenas"
            file_location = []
            for file in os.listdir(path):
                if file.endswith(".sol"): 
                    count += 1
                    file_location.append(f"{path}\{file}".strip())

            # para coletar o valor do autor e o nosso ao mesmo tempo,
            # vamos enviar para a função make_data_csv os dois input_data ao mesmo tempo
            row_list = [["Nome Instancia", "Solucao otima TSP", "Solucao TSPD Grafo Aux", "Tempo TSPD Grafo Aux", "Solucao TSPD Paper"]]
            input_data = []
            count_input = 0
            count = count/3
            with Bar('Processing...', max=count) as bar:
                for file in file_location:
                    # print(file)
                    if count_input == 0 and file.find("sMIP") == -1:
                        input_data.append(" \n")
                        count_input += 1
                    with open(file, 'r') as input_data_file:
                        input_data.append(input_data_file.read())
                    if count_input == 2:
                        row_list.append(make_data_csv(input_data, file)) 
                        bar.next()
                        input_data = []
                    count_input += 1
                    if count_input == 3:
                        count_input = 0 
                          
            name_path = path.split('\\')     
            with open(".\\data\\solutions\\sols_" + name_path[-2] + ".csv", 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(row_list)
            start = input("Deseja criar outro csv yes/no: ")


            