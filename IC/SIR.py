from tkinter import *
import time, random

#Variáveis globais
gridSize = 10 #tamanho de cada quadrado, cada célula
screenSize = 1000#tamanho da tela
numCells = int(screenSize/gridSize)

win = Canvas(Tk(),width = screenSize, height = screenSize) #definir tela

#Matriz que guarda as células (inicialmente todas as entradas nulas)
CA = [[0 for x in range(numCells)] for y in range(numCells)]

#matriz para contar tempo de recuperacao
R = [[0 for x in range(numCells)] for y in range(numCells)]

rec = 7 #iteracoes para recuperação
propagacao = 2 #individuos na vizinhança suficiente para propagação
#probabilidade = 3 #probabilidade de "nascer" com a doença


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
            infected = 0
            #contar quantidade de individuos propagacao
            if CA[(i+0)%numCells][(j+1)%numCells] == 1:
                infected += 1
            if CA[(i+0)%numCells][(j-1)%numCells] == 1:
                infected += 1
            if CA[(i+1)%numCells][(j+0)%numCells] == 1:
                infected += 1
            if CA[(i-1)%numCells][(j+0)%numCells] == 1:
                infected += 1
            if CA[(i+1)%numCells][(j+1)%numCells] == 1:
                infected += 1
            if CA[(i+1)%numCells][(j-1)%numCells] == 1:
                infected += 1
            if CA[(i-1)%numCells][(j+1)%numCells] == 1:
                infected += 1
            if CA[(i-1)%numCells][(j-1)%numCells] == 1:
                infected += 1

            if CA[i][j]==1: #verificar se a celular é infectada
                R[i][j] +=1

            if infected >= propagacao and CA[i][j] ==0 and R[i][j]<rec: #preencher matriz da proxima iteracao
                CAnext[i][j] = 1

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
    while Count()[0]<100:
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
        time.sleep(0.5)
        SIR()
        WriteData(filename, str(i), str(Count()[0]))
        WriteData(filename2, str(i), str(Count()[1]))

        


###
#Observações feitas:
#Para este modelo castrófico, não é possível uma pessoa não ser contaminada antes da extinção da doença
#Para que isto aconteça, todas sua vizinhança contaminada deve se curar antes de transmitir a doença,
#que é o mesmo que dizer se curar antes de estar doente.

#Para geração inicial da pop, se mais de 30% das pessoas estiverem contaminadas, então rapidamente todos estarão. 
#Consequentemente, todos irão ser imunes à doença iterações a frente (a depender de N*).