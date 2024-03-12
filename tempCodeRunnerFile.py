import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

dados = pd.read_excel('Dados_Clusterizados.xlsx')

# Convertendo MesReferencia para características numéricas
dados['AnoReferencia'] = dados['MesReferencia'].dt.year
dados['Mes'] = dados['MesReferencia'].dt.month

dados = dados[dados['Cluster'].isin([6, 7, 3, 2, 0])].reset_index(drop=True)

# Normalizar a variável alvo 'Valor'
scaler = MinMaxScaler()
dados['Valor'] = scaler.fit_transform(dados[['Valor']])

# Agrupar os dados pelo campo 'Cluster'
grupos_cluster = dados.groupby('Cluster')

# Inicializar um dicionário para armazenar os modelos treinados
modelos_treinados = {}

# Iterar por cada cluster e treinar um modelo de regressão
for cluster, dados_cluster in grupos_cluster:
    # Features (incluindo marca e modelo)
    X = dados[['AnoModelo', 'Salario', 'Inflacao_Total', 'Inflacao_Acumulada', 'Media_Dolar', 'Idade_modelo', 'Classificacao_Marca', 'Classificacao_Modelo', 'AnoReferencia', 'Mes']]

    # Variável alvo
    y = dados_cluster['Valor']
    
    # Codificar variáveis categóricas (marca e modelo)
    X = pd.get_dummies(X)
    
    # Realizar a validação cruzada
    modelo = LinearRegression()
    mse_scores = cross_val_score(modelo, X, y, cv=5, scoring='neg_mean_squared_error')
    mae_scores = cross_val_score(modelo, X, y, cv=5, scoring='neg_mean_absolute_error')
    
    # Converter os scores negativos para positivos
    mse_scores = -mse_scores
    mae_scores = -mae_scores
    
    # Imprimir as métricas de avaliação médias
    print(f"Cluster {cluster} - MSE médio: {mse_scores.mean()} - MAE médio: {mae_scores.mean()}")

    # Treinar o modelo com todos os dados do cluster
    modelo.fit(X, y)
    
    # Armazenar o modelo treinado
    modelos_treinados[cluster] = modelo
    
# Selecionar um cluster específico (por exemplo, cluster 7)
cluster_escolhido = 7

# Selecionar um modelo treinado para o cluster escolhido
modelo_escolhido = modelos_treinados[cluster_escolhido]

# Escolher um modelo aleatório de 'Classificacao_Modelo'
modelo_aleatorio = dados['Classificacao_Modelo'].sample(1).iloc[0]

# Selecionar os dados do cluster escolhido e modelo aleatório
dados_cluster_aleatorio = dados[(dados['Cluster'] == cluster_escolhido) & (dados['Classificacao_Modelo'] == modelo_aleatorio)]

# Features (incluindo marca e modelo)
X_teste = dados_cluster_aleatorio[['AnoModelo', 'Salario', 'Inflacao_Total', 'Inflacao_Acumulada', 'Media_Dolar', 'Idade_modelo', 'Classificacao_Marca', 'Classificacao_Modelo']]
# Variável alvo
y_teste = dados_cluster_aleatorio['Valor']

# Codificar variáveis categóricas (marca e modelo)
X_teste = pd.get_dummies(X_teste)

# Fazer previsões usando o modelo escolhido
y_pred = modelo_escolhido.predict(X_teste)

# Criar um gráfico de linha para comparar previsões com valores reais
plt.figure(figsize=(10, 6))
plt.plot(y_teste.values, label='Valor Real', marker='o')
plt.plot(y_pred, label='Previsão', marker='x')
plt.xlabel('Amostras')
plt.ylabel('Valor')
plt.title(f'Comparação entre Valor Real e Previsão para o Cluster {cluster_escolhido} e Modelo {modelo_aleatorio}')
plt.legend()
plt.show()