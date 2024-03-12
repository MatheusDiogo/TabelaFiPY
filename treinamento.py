import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler

dados = pd.read_excel('Dados_Clusterizados.xlsx')[['Valor', 'AnoModelo', 'Salario', 'Inflacao_Total', 'Inflacao_Acumulada', 'Media_Dolar', 'Classificacao_Marca', 'Classificacao_Modelo', 'Idade_modelo', 'Cluster']]

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
    X = dados_cluster[['AnoModelo', 'Salario', 'Inflacao_Total', 'Inflacao_Acumulada', 'Media_Dolar', 'Idade_modelo', 'Classificacao_Marca', 'Classificacao_Modelo']]
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