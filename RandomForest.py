import pandas as pd
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt

# Carregar os dados
dados = pd.read_excel('Dados_Clusterizados.xlsx')

# Convertendo MesReferencia para características numéricas
dados['AnoReferencia'] = dados['MesReferencia'].dt.year
dados['Mes'] = dados['MesReferencia'].dt.month

# Filtrar os clusters desejados
dados = dados[dados['Cluster'].isin([6, 7, 3, 2, 0])].reset_index(drop=True)

# Normalizar a variável alvo 'Valor'
scaler = MinMaxScaler()
dados['Valor'] = scaler.fit_transform(dados[['Valor']])

# Separar features e variável alvo
X = dados[['AnoModelo', 'Salario', 'Inflacao_Total', 'Inflacao_Acumulada', 'Media_Dolar', 'Idade_modelo', 'Classificacao_Marca', 'Classificacao_Modelo', 'AnoReferencia', 'Mes']]
y = dados['Valor']

# Criar uma transformação para variáveis categóricas
categorical_features = ['Classificacao_Marca', 'Classificacao_Modelo']
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

# Combinar transformações
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, categorical_features)
])

# Definir o modelo SVM
model_svm = SVR()

# Criar o pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model_svm)])

modelos_treinados = {}

# Definir os parâmetros para busca em grade
param_grid = {
    'model__kernel': ['linear', 'rbf'],
    'model__C': [0.1, 1, 10, 100],
    'model__gamma': [0.1, 1, 10, 100]
}

# Inicializar a busca em grade
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='neg_mean_squared_error')

grupos_cluster = dados.groupby('Cluster')

# Avaliação do modelo SVM para cada cluster
for cluster, dados_cluster in grupos_cluster:
    # Filtrar os dados para o cluster atual
    X = dados_cluster[['AnoModelo', 'Salario', 'Inflacao_Total', 'Inflacao_Acumulada', 'Media_Dolar', 'Idade_modelo', 'Classificacao_Marca', 'Classificacao_Modelo', 'AnoReferencia', 'Mes']]

    # Variável alvo
    y = dados_cluster['Valor']
    
    # Realizar a validação cruzada
    mse_scores = cross_val_score(pipeline, X, y, cv=5, scoring='neg_mean_squared_error')
    mae_scores = cross_val_score(pipeline, X, y, cv=5, scoring='neg_mean_absolute_error')
    
    # Converter os scores negativos para positivos
    mse_scores = -mse_scores
    mae_scores = -mae_scores
    
    # Imprimir as métricas de avaliação médias
    print(f"Cluster {cluster} - MSE médio: {mse_scores.mean()} - MAE médio: {mae_scores.mean()}")

    # Treinar o modelo com todos os dados do cluster
    pipeline.fit(X, y)
    
    # Armazenar o modelo treinado
    modelos_treinados[cluster] = pipeline

# Selecionar um cluster específico (por exemplo, cluster 7)
cluster_escolhido = 7

# Selecionar um modelo treinado para o cluster escolhido
modelo_escolhido = modelos_treinados[cluster_escolhido]

# Escolher um modelo aleatório de 'Classificacao_Modelo'
modelo_aleatorio = dados['Classificacao_Modelo'].sample(1).iloc[0]

# Selecionar os dados do cluster escolhido e modelo aleatório
dados_cluster_aleatorio = dados[(dados['Cluster'] == cluster_escolhido) & (dados['Classificacao_Modelo'] == modelo_aleatorio)]

# Features (incluindo marca e modelo)
X_teste = dados_cluster_aleatorio[['AnoModelo', 'Salario', 'Inflacao_Total', 'Inflacao_Acumulada', 'Media_Dolar', 'Idade_modelo', 'Classificacao_Marca', 'Classificacao_Modelo', 'AnoReferencia', 'Mes']]
# Variável alvo
y_teste = dados_cluster_aleatorio['Valor']

# Codificar variáveis categóricas (marca e modelo)
X_teste = pd.get_dummies(X_teste)

# Fazer previsões usando o modelo escolhido
y_pred = modelo_escolhido.predict(X_teste)

# Ordenar os dados pelo tempo
dados_cluster_aleatorio = dados_cluster_aleatorio.sort_values(by='MesReferencia')

# Criar uma nova figura
plt.figure(figsize=(10, 6))

# Plotar os valores reais
plt.plot(dados_cluster_aleatorio['MesReferencia'], y_teste.values, label='Valor Real', marker='o')

# Plotar as previsões
plt.plot(dados_cluster_aleatorio['MesReferencia'], y_pred, label='Previsão', marker='x')

# Configurar os rótulos do eixo x para os meses
plt.xticks(dados_cluster_aleatorio['MesReferencia'], rotation=45)

# Adicionar rótulos e título
plt.xlabel('Tempo')
plt.ylabel('Valor')
plt.title(f'Comparação entre Valor Real e Previsão para o Cluster {cluster_escolhido} e Modelo {modelo_aleatorio}')

# Adicionar legenda
plt.legend()

# Mostrar o gráfico
plt.show()