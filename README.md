# Heurísticas e Metaheurísticas para o TSPD

## Introdução

  O problema do caixeiro viajante com drones busca passar por todos os vértices de um grafo com um caminhão equipado com um drone. Sendo assim, temos vértices atendidos pelo caminhão e, possívelmente, vértices atendidos pelo drone, o que não é obrigatório.

## Algoritmos Usados

  Utilizamos heurísticas e metaheurísticas para resolver esse problema. Pensamos em um GRASP para o TSPD, com a fase construtiva contendo um algoritmo guloso-aleatorizado para resolver TSP e um algoritmo que adiciona entregas por drone nesse circuito do TSP. Como fase de intensificação utilizamos Busca Local.

## Como executar

  As instâncias do TSPD estão na pasta data/instances/, para executá-las, basta rodar $ Python tspd.py data/instances/"alguma instancia", substituir alguma instancia por alguma contida no diretório. 

## Instâncias

  Essas instâncias foram retiradas do artigo **Optimization Approaches for the Traveling Salesman Problem with Drone** de Agatz, Niels; Bouman, Paul; Schmidt, Marie (2018).
  
## Referências

AGATZ, Niels; BOUMAN, Paul; SCHMIDT, Marie. Optimization approaches for the traveling salesman problem with drone. Transportation Science, v. 52, n. 4, p. 965-981, 2018.
