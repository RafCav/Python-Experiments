import numpy as np
import matplotlib.pyplot as plt

#################### EXERCICIO
# Encontre os mínimos locais da função y = (x + 5)² começando do ponto x = 3.

def plot():
    # Define a função y = (x + 5)^2
    # def f(x):
    #     return (x + 5) ** 2
    f = lambda x: (x + 5) ** 2

    # Gera valores para x
    x = np.linspace(-10, 0, 500)  # Intervalo entre -10 e 0
    y = f(x)

    # Plota a função
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=r"$y = (x + 5)^2$", linewidth=2)
    plt.title("Gráfico da Função Original $y = (x + 5)^2$")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axhline(0, color='black', linewidth=0.8, linestyle="--")
    plt.axvline(0, color='black', linewidth=0.8, linestyle="--")
    plt.legend()
    plt.grid(alpha=0.4)
    plt.show()

#################### RESOLUÇÃO
# O algoritmo inicia com o parâmetro x=3
cur_x = 3

# Learning rate
rate = 0.01

# Define quando parar o algoritmo
precision = 0.000001  # Diferença entre os valores de x em 2 iterações consecutivas
max_iters = 10000  # Número máximo de iterações

previous_step_size = 1  # Inicializa o contador do passo anterior

iters = 0  # Contador de iterações

df = lambda x: 2*(x+5)  # Gradiente da Função

while previous_step_size > precision and iters < max_iters:

    prev_x = cur_x  # Armazena o valor corrente de x em prev_x

    cur_x = cur_x - rate * df(prev_x)  # Atualiza x na direção oposta ao gradiente, aplicando Gradiente Descendente

    previous_step_size = abs(cur_x - prev_x)  # Altera o valor de x

    iters += 1  # Incrementa o número de iterações

    print(f"Iteration: {iters} | x = {cur_x}")

print("\nO mínimo local da função ocorre em: ", cur_x)

plot()  # Esse plot é uma maneira visual de entender a função principal e o menor ponto de x