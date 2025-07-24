import numpy as np

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

def tau_gaussian(d, alpha=1):
    """Função de peso Gaussiana, definida como τ(d) = e^{-α d²}"""
    return np.exp(-alpha * d**2)

def weighted_kernel(radius, tau_fn):
    """
    Gera o kernel (matriz de pesos) aplicando a função τ sobre a matriz de distâncias.
    """
    dist = distance_matrix(radius)
    kernel = tau_fn(dist)
    kernel[np.isnan(dist)] = 0  # zera a célula central
    return kernel

def weighted_influence(grid, kernel):
    """
    Calcula o somatório ponderado de vizinhos infectados com base no kernel.
    """
    from scipy.signal import convolve2d
    infected = (grid == 1).astype(float)
    influence = convolve2d(infected, kernel, mode='same', boundary='fill', fillvalue=0)
    return influence


# Grid exemplo (0 = suscetível, 1 = infectado)
grid = np.array([
    [1, 0, 0],
    [0, 0, 0],
    [0, 0, 1]
])

radius = 1
alpha = 1

# Geração do kernel com função Gaussiana
kernel = weighted_kernel(radius, lambda d: tau_gaussian(d, alpha))

# Cálculo da influência ponderada
influence = weighted_influence(grid, kernel)

print("Kernel (τ(d)):\n", kernel)
print("Influência ponderada:\n", influence)
