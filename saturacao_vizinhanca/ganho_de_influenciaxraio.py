import numpy as np
import matplotlib.pyplot as plt

# --- Função peso tau(d) = 1/d ---
def tau_inverse(d):
    return 1 / d

# --- Gera matriz de distâncias euclidianas ---
def distance_kernel(radius):
    size = 2 * radius + 1
    center = radius
    dist = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            dx, dy = i - center, j - center
            if dx == 0 and dy == 0:
                dist[i, j] = np.nan
            else:
                dist[i, j] = np.sqrt(dx**2 + dy**2)
    return dist

# --- Soma total de pesos até certo raio ---
def total_weight_up_to_radius(max_radius, tau_fn):
    weights = []
    for r in range(1, max_radius + 1):
        dist = distance_kernel(r)
        tau = tau_fn(dist)
        tau[np.isnan(dist)] = 0
        weights.append(np.sum(tau))
    return weights

# --- Cálculo do ganho relativo ---
def gain_relative(weights):
    gains = []
    for i in range(1, len(weights)):
        delta = (weights[i] - weights[i-1]) / weights[i]
        gains.append(delta)
    return gains

# --- Encontra o raio de saturação ---
def find_saturation_radius(gains, threshold=0.10):
    for i, g in enumerate(gains):
        if g < threshold:
            return i + 2  # +2 porque índice 0 corresponde ao raio 2
    return None

# --- Parâmetros ---
max_radius = 30
weights = total_weight_up_to_radius(max_radius, tau_inverse)
gains = gain_relative(weights)
r_sat = find_saturation_radius(gains, threshold=0.10)

# --- Gráfico ---
plt.figure(figsize=(8, 5))
plt.plot(range(2, max_radius + 1), gains, marker='o', label='Ganho relativo')
if r_sat:
    plt.axvline(r_sat, color='green', linestyle='--', label=f'Saturação ≈ raio {r_sat}')
else:
    plt.text(10, 0.05, "Sem saturação até raio 30", color='red')

plt.title('Ganho relativo de influência por raio para $\\tau(d)=1/d$')
plt.xlabel('Raio da vizinhança')
plt.ylabel('Ganho relativo $(W_{r} - W_{r-1}) / W_{r}$')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
