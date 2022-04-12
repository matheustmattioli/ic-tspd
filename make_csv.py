# Neste script python vamos formar um csv das soluções obtidas 
# armazenadas nos arquivos:
# .\data\solutions\doublecenter
# .\data\solutions\singlecenter
# .\data\solutions\uniform

# Vamos formar um csv no formato:
# File name, author-value, our-value.

import csv
from pickle import GLOBAL
import sys
import os
from progress.bar import Bar 



def make_data_csv(input_data, file_name):
    # read data
    #print(input_data)
    tspd_value = input_data[0].split('\n')
    auth_data = input_data[1].split('\n')
    our_data = input_data[2].split('\n')

    # coleta info desejada
    auth_value = float(auth_data[0])
    our_value = float(our_data[0])
    
    our_time = float(our_data[1])
    tspd_value = str(tspd_value[0])

    # tratamento file_name
    file_name = file_name.split("\\")[5]
    file_name = file_name.split(".sol")[0]
    return [file_name, auth_value, our_value, our_time, tspd_value]


count = 0
# path = ".\\data\\solutions\\doublecenter"
path = ".\\data\\solutions\\filtered_data\\pequenas"
file_location = []
for file in os.listdir(path):
    if file.endswith(".sol"): 
        count += 1
        file_location.append(f"{path}\{file}".strip())
# print(os.listdir(path)[0], os.listdir(path)[1], os.listdir(path)[2])


path = ".\\data\\solutions\\filtered_data\\grandes"
for file in os.listdir(path):
    if file.endswith(".sol"):
        count += 1
        file_location.append(f"{path}\{file}".strip())


# para coletar o valor do autor e o nosso ao mesmo tempo,
# vamos enviar para a função make_data_csv os dois input_data ao mesmo tempo
row_list = [["Nome Instancia", "Solucao otima TSP", "Solucao GRASP TSP", "Tempo GRASP TSP", "Solucao TSPD"]]
input_data = []
count_input = 0
with Bar('Processing...', max=522) as bar:
    for file in file_location:
        #print(file)
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
        
with open(".\\data\\solutions\\sols.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(row_list)