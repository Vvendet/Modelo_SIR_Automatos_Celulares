import random

numCells = 100
CA = [[0 for x in range(numCells)] for y in range(numCells)]
for i in range(numCells):
	for j in range(numCells):
		if random.randint(1,100) < 20:
			CA[i][j] = 1
		else:
			CA[i][j] = 0

I = 0
S = 0
R = 0
for i in range(numCells): 
    for j in range(numCells):
        if CA[i][j] == 1:
            I += 1
        elif CA[i][j] == 0:
            S +=1

print(I)