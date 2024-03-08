import pandas as pd

data = pd.read_excel('Dados_Clusterizados.xlsx')

data = data[data['Cluster'] == 0]

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

data['Valor_suavizado'] = np.log(data['Valor'])

data = data.dropna()

# Criar uma figura com dois subplots
fig, axs = plt.subplots(1, 2, figsize=(18, 8))

# Plotar o mapa de calor da matriz de correlação
sns.heatmap(data.select_dtypes(include=['float64', 'int64']), annot=True, cmap='coolwarm', fmt=".2f", ax=axs[0])

# Plotar o gráfico de dispersão
from sklearn.linear_model import LinearRegression

# Ajustar uma regressão linear para cada categoria
regression = LinearRegression()
X = data['Idade_modelo'].values.reshape(-1)
y = data['Valor'].values
regression.fit(X, y)

# Plotar os gráficos de dispersão com as linhas de tendência para cada categoria
axs[0].plot(X, regression.predict(X), color='red', linewidth=2)
axs[0].scatter(data['Idade_modelo'], data['Valor'], alpha=0.5)
axs[0].set_title('Modelos Abaixo de 70 mil')
axs[0].set_xlabel('Idade do Modelo (meses)')
axs[0].set_ylabel('Valor dos Carros')
axs[0].grid(True)

axs[1].plot(X, regression.predict(X), color='red', linewidth=2)
axs[1].scatter(data['Idade_modelo'], data['Valor'], alpha=0.5)
axs[1].set_title('Modelos Acima de 70 mil')
axs[1].set_xlabel('Idade do Modelo (meses)')
axs[1].set_ylabel('Valor dos Carros')
axs[1].grid(True)

# Exibir o gráfico
plt.tight_layout()
plt.show()