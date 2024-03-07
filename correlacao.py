import pandas as pd

data = pd.read_excel('Dados_Tratados.xlsx')

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Aplicando LAG no valor do carro para acompanhar variação de Dolar, Inflação, Salário
data['Inflacao'] = data.groupby('Modelo')['Inflacao'].shift(1)
data['Inflacao'] = data['Inflacao'].apply(lambda x: x*100)

data['Valor_suavizado'] = np.log(data['Valor'])

data = data.dropna()

# Selecionar apenas as colunas numéricas
numeric_columns = data.select_dtypes(include=['float64', 'int64'])

# Calcular a matriz de correlação
correlation_matrix = numeric_columns.corr()

# Criar uma figura com dois subplots
fig, axs = plt.subplots(1, 2, figsize=(18, 6))

# Plotar o mapa de calor da matriz de correlação
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", ax=axs[0])
axs[0].set_title('Correlation Heatmap')

# Plotar o gráfico de dispersão
from sklearn.linear_model import LinearRegression

# Ajustar uma regressão linear
regression = LinearRegression()
X = data['Idade_modelo'].values.reshape(-1, 1)
y = data['Valor'].values
regression.fit(X, y)

# Plotar a linha de tendência
axs[1].plot(X, regression.predict(X), color='red', linewidth=2)
axs[1].scatter(data['Idade_modelo'], data['Valor'], alpha=0.5)
axs[1].set_title('Idade do Modelo vs. Valor dos Carros')
axs[1].set_xlabel('Idade do Modelo (meses)')
axs[1].set_ylabel('Valor dos Carros')
axs[1].grid(True)

# Exibir o gráfico
plt.tight_layout()
plt.show()