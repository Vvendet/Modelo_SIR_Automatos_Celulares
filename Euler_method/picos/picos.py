import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.optimize import minimize

# === Carrega os dados ===


# === Modelo SIR com metodo de Euler ===
def euler_sir(S0, I0, R0, beta, gamma, T, dt):
    n_steps = int(T / dt)
    S, I, R = [S0], [I0], [R0]
    t_values = [0.0]
    for _ in range(n_steps):
        s, i, r = S[-1], I[-1], R[-1]
        ds = -beta * s * i
        di = beta * s * i - gamma * i
        dr = gamma * i

        s_new = s + ds * dt
        i_new = i + di * dt
        r_new = r + dr * dt

        S.append(s_new)
        I.append(i_new)
        R.append(r_new)
        t_values.append(t_values[-1] + dt)

    return np.array(t_values), np.array(S), np.array(I), np.array(R)

# === Funcao de erro para otimizacao ===
def erro_quadratico_dois_parametros(params, S0, I0, R0, T, dt, t_ac, I_ac):
    beta, gamma = params
    if beta <= 0 or gamma <= 0:
        return np.inf
    t_modelo, _, I_modelo, _ = euler_sir(S0, I0, R0, beta, gamma, T, dt)
    interp_func = interp1d(t_modelo, I_modelo, kind='linear', bounds_error=False, fill_value="extrapolate")
    I_interp = interp_func(t_ac)
    erro = np.mean((I_interp - I_ac) ** 2)
    return erro


maiores_AC = []
maiores_IC = []

# === Maximos de cada grafico ===
for i in range(7):

    dados = np.loadtxt("media_desvioPadrao_o"+str(i+3) +".dat")
    tempo = dados[:4900001, 0]
    infectados = dados[:4900001, 1]
    #y_err = dados[:4900001,2]
    N = 10000
    I_ac = infectados / N

    # === Parametros iniciais ===
    I0 = I_ac[0]
    S0 = 1 - I0
    R0 = 0.0
    T = tempo[-1] + 1
    dt = 0.001
    params_iniciais = [0.2, 0.2]


    resultado = minimize(
        erro_quadratico_dois_parametros,
        x0=params_iniciais,
        bounds=[(0.01, 1.0), (0.01, 1.0)],
        args=(S0, I0, R0, T, dt, tempo, I_ac),
        method='L-BFGS-B'
    )

    beta_ajustado, gamma_ajustado = resultado.x
    t_euler, _, I_euler, _ = euler_sir(S0, I0, R0, beta_ajustado, gamma_ajustado, T, dt)
    I_interp = interp1d(t_euler, I_euler)(tempo)


    maiores_AC.append(max(I_ac))
    maiores_IC.append(max(I_interp))


# === Geracao do grafico ===
plt.figure(figsize=(10, 6))
plt.plot([3,4,5,6,7,8,9], maiores_AC, label="Picos modelo AC", color="blue", linewidth=2)
plt.plot([3,4,5,6,7,8,9], maiores_IC, label=f"Picos modelo IC", 
         color="red", linestyle="--", linewidth=2)
#plt.errorbar(tempo, I_ac_norm, yerr=y_err, fmt='o', label='Data with error bars', color='blue', ecolor='red', capsize=5)
plt.xlabel("ômegas")
plt.ylabel("Picos de Infectados")
plt.title("Comparacao entre Picos AC e IC")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
