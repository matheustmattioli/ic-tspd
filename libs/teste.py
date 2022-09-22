import numpy as np
import time


n = 10000000
# n = 10

start = time.time()
x = np.arange(0, n, 1)
end = time.time()
# print(x)
print(end - start)

start = time.time()
lista = [i for i in range(n)]
end = time.time()
# print(lista)
print(end - start)

start = time.time()
lista = []
for i in range(n):
    lista.append(i)
end = time.time()
# print(lista)
print(end - start)

start = time.time()
lista = n*[0]
for i in range(n):
    lista[i] = i
end = time.time()
# print(lista)
print(end - start)

start = time.time()
dicionario = {10*(n - i - 1):-i for i in range(n)}
end = time.time()
# print(dicionario)
print(end - start)

start = time.time()
for i in range(n - 1, -1, -1):
    if i in dicionario:
        # print(i)
        pass
end = time.time()
print(end - start)

start = time.time()
for i in range(n - 1, -1, -1):
    if dicionario.get(i):
        # print(i)
        pass
end = time.time()
print(end - start)

start = time.time()
for i in range(n - 1, -1, -1):
    if lista[i] == i:
        # print(i)
        pass
end = time.time()
print(end - start)

start = time.time()
for i in range(n - 1, -1, -1):
    if x[i] == i:
        # print(i)
        pass
end = time.time()
print(end - start)

# print(dicionario.pop(0))
start = time.time()
# for i in range(n - 1, -1, -1):
for i in range(n):
    v = dicionario.pop(10*i)
    # print(i, v)
    pass
end = time.time()
print(end - start)