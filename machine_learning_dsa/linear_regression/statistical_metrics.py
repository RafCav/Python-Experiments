import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_csv('pesos.csv')

# A Formula abaixo diz 'y ~ x' = variavel dependente ~ variavel independente
# Para mais de um x, usa-se 'y ~ x1 + x2 + x3'
estimativa = smf.ols(formula = 'Peso ~ Idade', data = df)  # Criando o Modelo de Regressão

modelo = estimativa.fit()  # Treinando o Modelo de Regressão

print(modelo.summary())
