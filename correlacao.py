import pandas as pd

data = pd.read_excel('Dados_Tratados.xlsx')

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

data['Valor_suavizado'] = np.log(data['Valor'])

data = data.dropna()

# Calcular a média do valor para cada modelo
modelo_mean = data.groupby('Modelo')['Valor'].mean()

# Dividir os modelos em duas categorias: abaixo de 70 mil e acima de 70 mil
modelos_abaixo_70mil = modelo_mean[modelo_mean < 70000].index
modelos_acima_70mil = modelo_mean[modelo_mean >= 70000].index

# Filtrar os dados com base nas categorias de modelos
data_abaixo_70mil = data[data['Modelo'].isin(modelos_abaixo_70mil)]
data_acima_70mil = data[data['Modelo'].isin(modelos_acima_70mil)]

# Selecionar apenas as colunas numéricas
numeric_columns_abaixo_70mil = data_abaixo_70mil.select_dtypes(include=['float64', 'int64'])
numeric_columns_acima_70mil = data_acima_70mil.select_dtypes(include=['float64', 'int64'])

# Calcular as matrizes de correlação para cada categoria
correlation_matrix_abaixo_70mil = numeric_columns_abaixo_70mil.corr()
correlation_matrix_acima_70mil = numeric_columns_acima_70mil.corr()

# Criar uma figura com dois subplots
fig, axs = plt.subplots(2, 2, figsize=(18, 8))

# Plotar o mapa de calor da matriz de correlação
sns.heatmap(correlation_matrix_abaixo_70mil.select_dtypes(include=['float64', 'int64']), annot=True, cmap='coolwarm', fmt=".2f", ax=axs[0, 0])

sns.heatmap(correlation_matrix_acima_70mil.select_dtypes(include=['float64', 'int64']), annot=True, cmap='coolwarm', fmt=".2f", ax=axs[0, 1])

# Plotar o gráfico de dispersão
from sklearn.linear_model import LinearRegression

# Ajustar uma regressão linear para cada categoria
regression_abaixo_70mil = LinearRegression()
X_abaixo_70mil = data_abaixo_70mil['Idade_modelo'].values.reshape(-1, 1)
y_abaixo_70mil = data_abaixo_70mil['Valor'].values
regression_abaixo_70mil.fit(X_abaixo_70mil, y_abaixo_70mil)

regression_acima_70mil = LinearRegression()
X_acima_70mil = data_acima_70mil['Idade_modelo'].values.reshape(-1, 1)
y_acima_70mil = data_acima_70mil['Valor'].values
regression_acima_70mil.fit(X_acima_70mil, y_acima_70mil)

# Plotar os gráficos de dispersão com as linhas de tendência para cada categoria
axs[1, 0].plot(X_abaixo_70mil, regression_abaixo_70mil.predict(X_abaixo_70mil), color='red', linewidth=2)
axs[1, 0].scatter(data_abaixo_70mil['Idade_modelo'], data_abaixo_70mil['Valor'], alpha=0.5)
axs[1, 0].set_title('Modelos Abaixo de 70 mil')
axs[1, 0].set_xlabel('Idade do Modelo (meses)')
axs[1, 0].set_ylabel('Valor dos Carros')
axs[1, 0].grid(True)

axs[1, 1].plot(X_acima_70mil, regression_acima_70mil.predict(X_acima_70mil), color='red', linewidth=2)
axs[1, 1].scatter(data_acima_70mil['Idade_modelo'], data_acima_70mil['Valor'], alpha=0.5)
axs[1, 1].set_title('Modelos Acima de 70 mil')
axs[1, 1].set_xlabel('Idade do Modelo (meses)')
axs[1, 1].set_ylabel('Valor dos Carros')
axs[1, 1].grid(True)

# Exibir o gráfico
plt.tight_layout()
plt.show()