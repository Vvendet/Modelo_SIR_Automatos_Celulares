import numpy as np
import time
import random
from tkinter import Tk, Canvas
from scipy.signal import convolve2d
import math

# === Parâmetros do modelo ===
grid_size = 10
screen_size = 1000
num_cells = screen_size // grid_size
rec = 5  # tempo de recuperação
theta = 9  # limiar de infecção equivalente a 1/d com Moore
radius = 11  # raio da vizinhança

def tau_inverse(d):
    return 1 / d

def tau_sqrt(d):
    return 1 / np.sqrt(d)

def distance_matrix(radius):
    size = 2 * radius + 1
    center = radius
    dist = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            dx = i - center
            dy = j - center
            if dx == 0 and dy == 0:
                dist[i, j] = np.nan
            else:
                dist[i, j] = np.sqrt(dx**2 + dy**2)
    return dist

def weighted_kernel(radius, tau_fn):
    dist = distance_matrix(radius)
    kernel = tau_fn(dist)
    kernel[np.isnan(dist)] = 0
    return kernel

kernel = weighted_kernel(radius, tau_inverse)

def initialize_population(pop_size):
    CA = np.zeros((num_cells, num_cells), dtype=int)
    R = np.zeros_like(CA)
    count = 0
    while count < pop_size:
        i = np.random.randint(0, num_cells)
        j = np.random.randint(0, num_cells)
        if CA[i, j] == 0:
            CA[i, j] = 1
            count += 1
    return CA, R

def update_CA(CA, R):
    influence = convolve2d((CA == 1).astype(float), kernel, mode='same', boundary='fill', fillvalue=0)
    new_CA = np.zeros_like(CA)
    new_R = R.copy()

    infected = (CA == 1)
    susceptible = (CA == 0) & (R == 0)

    new_R[infected] += 1
    new_CA[susceptible & (influence >= theta)] = 1
    new_CA[infected & (new_R < rec)] = 1

    return new_CA, new_R

def count_infected(CA):
    return np.sum(CA == 1)

def run_simulation(generations=50, initial_infected=500, visual=True):
    CA, R = initialize_population(initial_infected)
    
    if visual:
        root = Tk()
        canvas = Canvas(root, width=screen_size, height=screen_size)
        canvas.pack()

    with open("infectados.dat", "w") as f:
        for gen in range(generations):
            if visual:
                canvas.delete("all")
                for i in range(num_cells):
                    for j in range(num_cells):
                        if CA[i, j] == 1:
                            x1, y1 = j * grid_size, i * grid_size
                            canvas.create_rectangle(x1, y1, x1+grid_size, y1+grid_size, fill='red')
                canvas.update()
                time.sleep(0.5)

            CA, R = update_CA(CA, R)
            f.write(f"{gen}\t{count_infected(CA)}\n")

    if visual:
        root.mainloop()

if __name__ == '__main__':
    # Escolha entre modo visual (True) ou rápido (False)
    run_simulation(generations=100, initial_infected=700, visual=False)
