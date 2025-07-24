import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parâmetros da simulação
size = 101    # Número de células por linha
steps = 100   # Número de gerações

# Inicializar grade
grid = np.zeros((steps, size), dtype=int)
grid[0, size // 2] = 1  # célula central ativa

# Criar a figura
fig, ax = plt.subplots()
im = ax.imshow(grid, cmap='binary', interpolation='nearest', animated=True)
ax.set_title("Regra 90 — Autômato Celular 1D")
ax.set_xlabel("Células")
ax.set_ylabel("Tempo")

# Função de atualização para cada frame
def update(frame):
    if frame == 0:
        return [im]
    for i in range(1, size - 1):
        left = grid[frame - 1, i - 1]
        right = grid[frame - 1, i + 1]
        grid[frame, i] = left ^ right
    im.set_data(grid)
    return [im]

# Criar animação
ani = animation.FuncAnimation(
    fig, update, frames=steps, interval=100, blit=True, repeat=False
)

plt.tight_layout()
plt.show()
