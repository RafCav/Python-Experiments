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
import matplotlib as mpl

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

    media_target = df['target'].mean()
    media_rm = df['RM'].mean()
    mean_y = scatter_plot.plot(x_range, [media_target, media_target], '--', color='red', linewidth=1)
    mean_x = scatter_plot.plot([media_rm, media_rm], y_range, '--', color='red', linewidth=1)

    plt.show()


def main():
    # ################################### DATASET IMPORT
    data = pd.read_csv('HousingData.csv', sep=',')
    data = data.rename(columns={'MEDV': 'target'})

    print(f"Prévia do Dataset:\n{data.head()}\n")

    sum_of_squared_errors(data)

    standard_deviation(data)

    correlation(data)


main()
