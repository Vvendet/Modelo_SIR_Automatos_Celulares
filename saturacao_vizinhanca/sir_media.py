import numpy as np
import time
import random
from tkinter import Tk, Canvas
from scipy.signal import convolve2d

# === Parâmetros do modelo ===
grid_size = 10
screen_size = 1000
num_cells = screen_size // grid_size
rec = 10  # tempo de recuperação
alpha = 26.5  # limiar de infecção equivalente a 1/d com Moore
radius = 15  # raio da vizinhança

def tau_inverse(d):
    return 1 / d
def tau_sqrt(d):
    return 1 / (np.sqrt(d))
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

def weighted_kernel(radius, tau_fn):
    dist = distance_kernel(radius)
    kernel = tau_fn(dist)
    kernel[np.isnan(dist)] = 0
    return kernel

kernel = weighted_kernel(radius, tau_sqrt)

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
    new_CA[susceptible & (influence >= alpha)] = 1
    new_CA[infected & (new_R < rec)] = 1

    return new_CA, new_R

def count_infected(CA):
    return np.sum(CA == 1)

def run_simulation(generations=50, initial_infected=700, visual=True, export=False, run_id=1):
    CA, R = initialize_population(initial_infected)

    if visual:
        root = Tk()
        canvas = Canvas(root, width=screen_size, height=screen_size)
        canvas.pack()

    filename = f"infectados{run_id}.dat"
    with open(filename, "w") as f:
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

def compute_average_std(filenames, output_filename):
    data = [np.loadtxt(fname)[:,1] for fname in filenames]
    data = np.array(data)
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0)
    generations = np.arange(data.shape[1])

    with open(output_filename, 'w') as f:
        for gen, m, s in zip(generations, mean, std):
            f.write(f"{gen}\t{m:.2f}\t{s:.2f}\n")

if __name__ == '__main__':
    simulations = 5
    generations = 100
    for run in range(1, simulations + 1):
        run_simulation(generations=generations, initial_infected=700, visual=False, run_id=run)

    filenames = [f"infectados{i}.dat" for i in range(1, simulations + 1)]
    compute_average_std(filenames, "media_infectados.dat")
