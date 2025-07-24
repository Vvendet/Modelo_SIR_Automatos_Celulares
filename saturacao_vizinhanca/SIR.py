from tkinter import *
import time, random
import math
import numpy as np
from scipy.signal import convolve2d

#Variáveis globais
gridSize = 10 #tamanho de cada quadrado, cada célula
screenSize = 1000#tamanho da tela
numCells = int(screenSize/gridSize)

win = Canvas(Tk(),width = screenSize, height = screenSize) #definir tela

#Matriz que guarda as células (inicialmente todas as entradas nulas)
CA = [[0 for x in range(numCells)] for y in range(numCells)]

#matriz para contar tempo de recuperacao
R = [[0 for x in range(numCells)] for y in range(numCells)]

rec = 10 #iteracoes para recuperação
propagacao = 3 #individuos na vizinhança suficiente para propagação
#probabilidade = 3 #probabilidade de "nascer" com a doença


# === Funcao para calcular distancia ===

def distance_matrix(radius):
    """
    Gera uma matriz de distâncias euclidianas para uma vizinhança de dado raio.
    O centro (célula-alvo) está na posição (radius, radius).
    """
    size = 2 * radius + 1
    center = radius
    dist = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            dx = i - center
            dy = j - center
            if dx == 0 and dy == 0:
                dist[i, j] = np.nan  # ignora a célula central
            else:
                dist[i, j] = np.sqrt(dx**2 + dy**2)
    return dist

# -------------------------
# Funções τ(d)
# -------------------------

def tau_gaussian(d, alpha=1):
    return np.exp(-alpha * d**2)

def tau_exponential(d, alpha=1):
    return np.exp(-alpha * d)

def tau_inverse(d):
    return 1 / d

def tau_inverse_squared(d):
    return 1 / d**2

def tau_inverse_quadratic(d):
    return 1 / (1 + d**2)

# -------------------------
# Geração do kernel e cálculo da influência
# -------------------------

def weighted_kernel(radius, tau_fn):
    """
    Aplica a função τ(d) sobre a matriz de distâncias.
    """
    dist = distance_matrix(radius)
    kernel = tau_fn(dist)
    kernel[np.isnan(dist)] = 0  # zera a célula central
    return kernel

def weighted_influence_at_cell(grid, row, col, radius, tau_fn):
    """
    Calcula a influência ponderada recebida por uma célula específica (row, col).
    
    grid    : array 2D com estados (0: suscetível, 1: infectado, ...)
    row, col: coordenadas da célula a ser avaliada
    radius  : raio da vizinhança considerada
    tau_fn  : função de peso baseada na distância (ex: tau_inverse, tau_gaussian)
    
    Retorna: float com a soma dos pesos de vizinhos infectados
    """
    total = 0.0
    grid = np.asarray(grid) 
    rows, cols = grid.shape

    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            ni, nj = row + dx, col + dy
            if dx == 0 and dy == 0:
                continue  # ignora a célula central
            if 0 <= ni < rows and 0 <= nj < cols:
                if grid[ni, nj] == 1:  # se vizinho está infectado
                    d = np.sqrt(dx**2 + dy**2)
                    total += tau_fn(d)
    
    return total
def weighted_influence(grid, kernel):
    """
    Calcula a influência ponderada por convolução com o kernel de pesos.
    """
    infected = (grid == 1).astype(float)
    return convolve2d(infected, kernel, mode='same', boundary='fill', fillvalue=0)


def weighted_influence_at(grid, row, col, kernel):
    """
    Retorna a influência ponderada total recebida por uma célula (row, col)
    com base nos vizinhos infectados e um kernel de pesos.

    grid   : grade 2D com estados (0: suscetível, 1: infectado, ...)
    row, col : coordenadas da célula a analisar
    kernel : matriz de pesos τ(d)
    """
    radius = kernel.shape[0] // 2
    total = 0.0
    for i in range(-radius, radius + 1):
        for j in range(-radius, radius + 1):
            if i == 0 and j == 0:
                continue  # ignora a célula central
            ni, nj = row + i, col + j
            if 0 <= ni < grid.shape[0] and 0 <= nj < grid.shape[1]:
                if grid[ni, nj] == 1:  # infectado
                    total += kernel[i + radius, j + radius]
    return total

def update(ind):

    frame = frames[ind]
    ind += 1
    if ind == frameCnt:
        ind = 0
    label.configure(image=frame)
    root.after(100, update, ind)

#limpa a tela e inicia
def InitCanvas():
    win.delete('all')

    #draw grid
    for i in range(numCells): #desenhar as linhas para a tabela
        win.create_line(0,gridSize * i, screenSize, gridSize * i)
        win.create_line(gridSize * i, 0, gridSize * i, screenSize)
    win.pack()

def RefreshGrid(): #função para atualizar a tela
    global CA

    InitCanvas()

    #desenha o retangulo vermelho, se a celula é infectada
    for i in range(numCells):
        for j in range(numCells):
            if CA[i][j] == 1:
                x1 = gridSize * i
                y1 = gridSize * j
                win.create_rectangle(x1,y1,x1+gridSize,y1+gridSize,fill='red') 
    win.update()

def SIR(): #aplicar as regras em cada celula
    global CA, R, rec

    CAnext = [[0 for x in range(numCells)] for y in range(numCells)] #definir matriz da proxima iteracao

    for i in range(numCells): 
        for j in range(numCells):
            if CA[i][j]==1: #verificar se a celular é infectada
                R[i][j] +=1

            if CA[i][j] == 0 and weighted_influence_at_cell(CA,i,j,4,tau_inverse)>=6.828 and R[i][j]==0:
                CAnext[i][j]=1
            elif CA[i][j] ==1 and R[i][j]>=rec:
                CAnext[i][j]=0
            else:
                CAnext[i][j] = CA[i][j]

    CA = CAnext
    RefreshGrid()
            
def Count(): #função para contar a quantidade de infectados e suscetíveis
    global CA
    I = 0
    S = 0
    R = 0
    for i in range(numCells): 
        for j in range(numCells):
            if CA[i][j] == 1:
                I += 1
            elif CA[i][j] == 0:
                S +=1

    return I, S

def WriteData(file, message1, message2): #função para escrever os dados nos arquivos

    with open(file,'a') as file:
        file.write(f"{message1}    ")
        file.write(f"{message2}\n")


                
if __name__ == '__main__':
    """
    #gerar as celulas aleatoriamente
    for i in range(numCells):
        for j in range(numCells):
            if random.randint(1,100) < probabilidade:
                CA[i][j] = 1
            else:
                CA[i][j] = 0

    """

    #Gerar 100 indivíduos infectados
    while Count()[0]<700:
        n1 = random.randint(0,numCells-1)
        n2 = random.randint(0,numCells-1)
        if CA[n1][n2]==0:
            CA[n1][n2]=1
        else:
            pass


    RefreshGrid()

    generations = 50

    filename = 'infectados.dat' #Arquivo de saída para relacionar tempo x infectados
    filename2 = 'sadios.dat'#Arquivo de saída para relacionar tempo x sadios
    for i in range(generations):
        time.sleep(1)
        SIR()
        WriteData(filename, str(i), str(Count()[0]))
        


###
#Observações feitas:
#Para este modelo castrófico, não é possível uma pessoa não ser contaminada antes da extinção da doença
#Para que isto aconteça, todas sua vizinhança contaminada deve se curar antes de transmitir a doença,
#que é o mesmo que dizer se curar antes de estar doente.

#Para geração inicial da pop, se mais de 30% das pessoas estiverem contaminadas, então rapidamente todos estarão. 
#Consequentemente, todos irão ser imunes à doença iterações a frente (a depender de N*).