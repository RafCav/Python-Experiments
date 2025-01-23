
# OBS: Este exercício não usa funções estatisticas, apenas matematica :)

# Parte 1: Desenvolva o código necessário para a fórmula básica da regressão linear simples, calculando os coeficientes.
# Parte 2: Use o modelo para fazer previsões.

# O dataset abaixo contém dados sobre medidas da cabeça de seres humanos e o peso do cérebro.
# Seu trabalho é criar um modelo de regressão linear simples que receba uma medida como entrada e faça a previsão do peso do cérebro!

import numpy as np
import pandas as pd

data = pd.read_csv('pesos2.csv')
print(f"Meus Dados:\n{data.head()}\n")

X = data['Head Size'].values  # Lista de valor de X
Y = data['Brain Weight'].values  # Lista de valor de Y

# Parte 1: Calculando os Coeficientes
# Lembrando que a formula para a regressão linear é y = a + bx
# Os melhores valores de a e b devem surgir agora.

# Como calcular b (inclinação)?
# A formula para a inclinação é: (X[i] - mean_x) * (Y[i] - mean_y) / (X[i] - mean_x)²
# [i] significa que temos que passar por toda a base de teste
# Vamos separar o calculo em numerador e denominador:

mean_x = np.mean(X)  # Média de X
mean_y = np.mean(Y)  # Média de Y
numer = 0  # numerador
denom = 0  # denominador

for i in range(len(X)):
    numer += (X[i] - mean_x) * (Y[i] - mean_y)
    denom += (X[i] - mean_x) ** 2

b = numer / denom

# Com isso temos o melhor valor para b, agora podemos calcular para a
# 'a' é o intercepto, ou seja, garante que a linha passe pelo "centro dos dados"
# a formula do intercepto é: a = mean_y - b * mean_x

a = mean_y - (b * mean_x)

print(f"Melhor valor de a: {a} | Melhor valor de b: {b}")

# Parte 2: Fazendo previsões
x_novo = 4450  # Meu novo valor fora do conjunto de dados
y_previsto = a + (b * x_novo)

print(f"\nPara um cérebro de tamanho: {x_novo} → Seu peso projetado é de {y_previsto} g")

