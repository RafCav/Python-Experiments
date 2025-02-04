"""
Definindo o Problema de Negócio
Nosso objetivo é construir um modelo de Machine Learning que seja capaz de fazer previsões sobre a taxa média de
ocupação de casas na região de Boston, EUA, por proprietários. A variável a ser prevista é um valor numérico que
representa a mediana da taxa de ocupação das casas em Boston. Para cada casa temos diversas variáveis explanatórias.
Sendo assim, podemos resolver este problema empregando Regressão Linear Simples ou Múltipla.

Definindo o Dataset
Usaremos o Boston Housing Dataset, que é um conjunto de dados que tem a taxa média de ocupação das casas, juntamente com
outras 13 variáveis que podem estar relacionadas aos preços das casas. Esses são os fatores como condições
socioeconômicas, condições ambientais, instalações educacionais e alguns outros fatores semelhantes. Existem 506
observações nos dados para 14 variáveis. Existem 12 variáveis numéricas em nosso conjunto de dados e 1 variável
categórica. O objetivo deste projeto é construir um modelo de regressão linear para estimar a taxa média de ocupação das
casas pelos proprietários em Boston.

CRIM: per capita crime rate by town
ZN: proportion of residential land zoned for lots over 25,000 sq.ft.
INDUS: proportion of non-retail business acres per town
CHAS: Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)
NOX: nitric oxides concentration (parts per 10 million)
RM: average number of rooms per dwelling
AGE: proportion of owner-occupied units built prior to 1940
DIS: weighted distances to five Boston employment centres
RAD: index of accessibility to radial highways
TAX: full-value property-tax rate per 10,000
PTRATIO: pupil-teacher ratio by town
B: 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town
LSTAT: % lower status of the population
MEDV: Median value of owner-occupied homes in $1000's

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.stats import zscore
import statsmodels.api as sm
from sklearn import linear_model
from sklearn.datasets import make_regression
import matplotlib as mpl
import time

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def sum_of_squared_errors(df):
    """
    SSE é uma métrica usada em Machine Learning para medir a diferença entre os valores reais e os valores previstos
    por um modelo. Ele é calculado somando o quadrado de cada erro (diferença entre valor real e previsto). Quanto menor
    o SSE, melhor o ajuste do modelo aos dados.

    Benefícios do SSE:
    1. Se o erro for alto, o modelo não está prevendo bem e pode precisar de ajustes.
    2. Comparando diferentes modelos pelo erro, podemos escolher o mais preciso.
    3. Um erro muito baixo pode indicar que o modelo decorou os dados (overfitting), enquanto um erro muito alto pode
    significar que ele não aprendeu bem (underfitting).
    4. Modelos mais precisos geram previsões mais confiáveis para aplicações do mundo real, como previsão de vendas,
    diagnósticos médicos, etc
    """
    # Média da coluna "target"
    valor_medio_esperado_na_previsao = df['target'].mean()

    # Valor da coluna target (linha a linha) menos média da coluna ao quadrado
    squared_errors = pd.Series(valor_medio_esperado_na_previsao - df['target'])**2

    # SSE vai ser a soma dos erros
    sse = np.sum(squared_errors)

    print(f"Soma dos Quadrados dos Erros (SSE): {sse:.0f}")

    hist_plot = squared_errors.plot(kind='hist')
    plt.show()


def standard_deviation(df):
    """
    Para uma Regressão Linear Simples, escolhi o campo RM (número médio de quartos por residência). Abaixo vou calcular o
    desvio padrão do campo.

    O desvio padrão mede a dispersão dos valores em relação à média.
    Desvio padrão baixo: Significa que os valores estão mais próximos da média, ou seja, há menos variação.
    Isso pode ser bom se você deseja um conjunto de dados mais uniforme, mas também pode indicar falta de diversidade nos
    dados.

    Desvio padrão alto: Indica maior variação nos valores. Isso pode ser útil se você quiser um modelo mais generalizável,
    mas também pode trazer desafios, como a necessidade de normalizar os dados antes da regressão.
    """
    print(f"Desvio Padrão do campo RM: {np.std(df['RM']):.5f}")


def correlation(df):
    """
    O coeficiente de correlação de Pearson, criado pelo estatístico Karl Pearson, mede a relação linear entre duas
    variáveis e indica quão bem uma variável pode prever a outra. O resultado varia de -1 a 1:
    """

    # pearsonr me retorna o coeficiente de correlação de Pearson e o valor p
    # o valor p indica a probabilidade de essa correlação ter ocorrido por acaso
    # Como só queremos a correlação, buscamos por [0].
    print(f"Correlação RM x target: {pearsonr(df['RM'], df['target'])[0]:.5f}")

    # Plot da correlação entre RM e Target
    x_range = [df['RM'].min(), df['RM'].max()]
    y_range = [df['target'].min(), df['target'].max()]

    scatter_plot = df.plot(kind='scatter', x='RM', y='target', xlim=x_range, ylim=y_range)
    plt.title("Correlação entre RM e Target")

    media_target = df['target'].mean()
    media_rm = df['RM'].mean()
    mean_y = scatter_plot.plot(x_range, [media_target, media_target], '--', color='red', linewidth=1)
    mean_x = scatter_plot.plot([media_rm, media_rm], y_range, '--', color='red', linewidth=1)

    plt.show()


def linear_regression_statsmodels(df):
    y = df['target']
    x = df['RM']

    """
    A equação da regressão linear é dada por: y = β0 + β1x + e, onde β0 é a constante (termo de intercepto) e β1 é o 
    coeficiente da variável independente x.
    
    Por padrão, o statsmodels NÃO adiciona automaticamente essa constante ao modelo, sendo necessário adicioná-la 
    manualmente. A função abaixo faz exatamente isso.
    """
    x = sm.add_constant(x)

    # Criando o modelo de regressão
    modelo = sm.OLS(y, x)

    # Treinando o modelo
    modelo_v1 = modelo.fit()

    print(f"Resultado Modelo V1:\n{modelo_v1.summary()}\n")
    # print(modelo_v1.params)  # Aqui são as constantes, já exibido acima, mas aqui ta mais limpo

    # Mostrando previsão durante o treinamento
    valores_previstos_treino = modelo_v1.predict(x)
    print(f"Valores Previstos pelo modelo durante o treino:\n{valores_previstos_treino.head(5)}\n")

    # Mostrando previsão para um x = 5 (novo valor)
    new_rm = 5
    xp = np.array([1, new_rm])  # Tenho que passar o coeficiente, como uma matriz, já expliquei acima.
    print(f"Novo Dado X = {new_rm} | Y Previsto = {modelo_v1.predict(xp)[0]:.1f}")

    # Scatter Plot com a linha de regressão
    x_range = [df['RM'].min(), df['RM'].max()]
    y_range = [df['target'].min(), df['target'].max()]

    scatter_plot = df.plot(kind='scatter', x='RM', y='target', xlim=x_range, ylim=y_range)
    plt.title("Regressão Linear com StatsModels")

    media_target = df['target'].mean()
    media_rm = df['RM'].mean()
    mean_y = scatter_plot.plot(x_range, [media_target, media_target], '--', color='red', linewidth=1)
    mean_x = scatter_plot.plot([media_rm, media_rm], y_range, '--', color='red', linewidth=1)
    regression_line_plt = scatter_plot.plot(df['RM'], valores_previstos_treino, '-', color='orange', linewidth=2)

    plt.show()

    residuos = df['target'] - valores_previstos_treino
    """
    A padronização (Z-score) converte os dados para uma escala com média 0 e desvio padrão 1.  
    Isso ajuda na análise estatística, facilita a interpretação dos resíduos e melhora a detecção de outliers.
    """
    residuos_normalizados = zscore(residuos)  # Padroniza os dados

    # plot residuos
    residual_scatter_plot = plt.plot(df['RM'], residuos_normalizados, 'bp')
    plt.xlabel('RM')
    plt.ylabel('Resíduos Normalizados')
    plt.title("Resíduos do modelo V1 (StatsModels)")
    mean_residual = plt.plot([int(x_range[0]), round(x_range[1], 0)], [0, 0], '-', color='red', linewidth=3)
    upper_bound = plt.plot([int(x_range[0]), round(x_range[1], 0)], [3, 3], '--', color='red', linewidth=2)
    lower_bound = plt.plot([int(x_range[0]), round(x_range[1], 0)], [-3, -3], '--', color='red', linewidth=2)
    plt.grid()
    plt.show()


def linear_regression_scikit_learn(df):
    # Cria o objeto
    modelo_v2 = linear_model.LinearRegression(fit_intercept=True)

    """
    No Scikit-Learn (e ML no geral), X deve ser uma matriz (array 2D) com formato (n_amostras, n_features).
    Isso porque os modelos precisam distinguir entre observações (linhas) e características (colunas).
    Se X for um vetor 1D, usamos reshape(-1, 1) para transformá-lo em uma matriz 2D
    """

    # Dados de entrada e saída
    num_observ = len(df)
    x = df['RM'].values.reshape((num_observ, 1))  # X deve sempre ser uma matriz e nunca um vetor
    y = df['target'].values  # y pode ser um vetor

    print(f"\nTipo de dado (x): {type(x)} | Dimensões: {np.ndim(x)}")
    print(f"Tipo de dado (y): {type(y)} | Dimensões: {np.ndim(y)}")

    """
    df['column'].values → Converte a coluna em um array NumPy
    .reshape((num_observ, 1)) → Transforma o array 1D em uma matriz 2D com num_observ linhas e 1 única coluna
    Como y representa o alvo (variável dependente), ele pode ser um vetor 1D
    """

    # Treinamento
    modelo_v2.fit(x, y)

    print(f"\nCoeficiente: {modelo_v2.coef_}\nIntercepto: {modelo_v2.intercept_}")
    # print(modelo_v2.predict(x))  # Dados que foram previstos pelo modelo durante o treinamento

    # Mostrando previsão para um x = 5 (novo valor)
    new_rm = 5
    xp = np.array(new_rm).reshape(-1, 1)
    print(f"\nNovo Dado X = {new_rm} | Y Previsto = {modelo_v2.predict(xp)[0]:.1f}")

    """
    O -1 do reshape é como um coringa: ele indica que o NumPy deve calcular automaticamente o número de linhas com base 
    nos dados.
    """


def compara_pacotes():
    # Gera um conjunto de dados sintético para regressão
    hx, hy = make_regression(
        n_samples=10000000,  # Número de amostras (10 milhões de exemplos)
        n_features=1,  # Cada amostra tem 1 única feature (variável independente)
        n_targets=1,  # Apenas 1 variável alvo (output/dependente)
        random_state=101  # Define a seed para reprodutibilidade dos resultados (opcional)
    )
    """
    hx será uma matriz (10 milhões de linhas, 1 coluna) representando as features
    hy será um vetor (10 milhões de valores) representando os valores-alvo da regressão
    """

    print("Comparação StatsModels x ScikitLearn")

    st = time.time()
    sk_linear_regression = linear_model.LinearRegression(fit_intercept=True)
    sk_linear_regression.fit(hx, hy)
    et = time.time()
    print(f"SciKit: {et - st:.5f} segundos")

    st = time.time()
    sm_linear_regression = sm.OLS(hy, sm.add_constant(hx))
    sm_linear_regression.fit()
    et = time.time()
    print(f"StatsModels: {et - st:.5f} segundos")


def main():
    # ################################### DATASET IMPORT
    data = pd.read_csv('HousingData.csv', sep=',')
    data = data.rename(columns={'MEDV': 'target'})

    print(f"Prévia do Dataset:\n{data.head()}\n")

    # sum_of_squared_errors(data)

    # standard_deviation(data)

    # correlation(data)

    # linear_regression_statsmodels(data)

    # linear_regression_scikit_learn(data)

    compara_pacotes()


main()
