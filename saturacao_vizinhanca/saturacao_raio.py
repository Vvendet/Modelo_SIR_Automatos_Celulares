import numpy as np
import matplotlib.pyplot as plt
import math

def tau_inverse(d):
    return 1 / d


def tau_sqrt(d):
    return 1 / np.sqrt(d)

def distance_kernel(radius):
    size = 2 * radius + 1
    center = radius
    dist = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            dx, dy = i - center, j - center
            if dx == 0 and dy == 0:
                dist[i, j] = np.nan  # ignora a célula central
            else:
                dist[i, j] = np.sqrt(dx**2 + dy**2)
    return dist

def total_weight_up_to_radius(max_radius, tau_fn):
    weights = []
    for r in range(1, max_radius + 1):
        dist = distance_kernel(r)
        tau = tau_fn(dist)
        tau[np.isnan(dist)] = 0
        weights.append(np.sum(tau))
    return weights

def saturation_radius(weights, epsilon=0.10):
    for r in range(1, len(weights)):
        delta = (weights[r] - weights[r-1]) / weights[r]
        if delta < epsilon:
            return r + 1  # raio real é índice + 1
    return None

# === Parâmetros
max_radius = 30
weights = total_weight_up_to_radius(max_radius, tau_inverse)
r_sat_10 = saturation_radius(weights, epsilon=0.05)

# === Gráfico
plt.figure(figsize=(8, 5))
plt.plot(range(1, max_radius + 1), weights, marker='o', label='Soma acumulada')

if r_sat_10:
    plt.axvline(r_sat_10, color='green', linestyle='--', label=f'Saturação ≈ raio {r_sat_10} (ganho < 5%)')
else:
    plt.text(10, weights[-1]*0.7, "Sem saturação até raio 30", color='red')

plt.title('Soma acumulada dos pesos τ(d) = 1/d por raio de vizinhança')
plt.xlabel('Raio da vizinhança')
plt.ylabel('Peso total acumulado')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
