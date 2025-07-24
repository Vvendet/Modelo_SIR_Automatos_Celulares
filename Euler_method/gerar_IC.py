import random

numCells = 100
I0 = 900
CA = [[0 for x in range(numCells)] for y in range(numCells)]
I = 0


def ContarInfectados():
	global CA
	contador = 0 
	for i in range(numCells): 
	    for j in range(numCells):
	        if CA[i][j] == 1:
	            contador += 1
	return contador

while (I<I0):
	for i in range(numCells):
		for j in range(numCells):
			if (random.randint(1,100) <= 10) and (ContarInfectados()<=I0):
				CA[i][j] = 1
			else:
				CA[i][j] = 0
	I = ContarInfectados()
	

print(CA)
print(I)