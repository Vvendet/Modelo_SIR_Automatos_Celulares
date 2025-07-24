import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Parâmetros do modelo
beta = 0.4   # taxa de infecção
gamma = 0.1  # taxa de recuperação
N = 1.0      # população total (normalizada)

# Condições iniciais
I0 = 0.01    # 1% infectado
R0 = 0.0     # 0% recuperado
S0 = N - I0 - R0

# Intervalo de tempo (dias)
t = np.linspace(0, 160, 1000)

# Equações diferenciais do modelo SIR
def sir(y, t, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I
    return [dSdt, dIdt, dRdt]

# Resolver as EDOs
y0 = [S0, I0, R0]
sol = odeint(sir, y0, t, args=(beta, gamma))
S, I, R = sol.T

# Plotar o gráfico
plt.figure(figsize=(10,6))
plt.plot(t, S, 'b-', label='Suscetíveis (S)')
plt.plot(t, I, 'r-', label='Infectados (I)')
plt.plot(t, R, 'gray', label='Removidos (R)')
plt.xlabel('Tempo (dias)')
plt.ylabel('Proporção da população')
plt.title('Modelo SIR — Evolução temporal')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('sir_grafico.png', dpi=300)
plt.show()
