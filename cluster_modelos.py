import pandas as pd
import matplotlib.pyplot as plt
from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series_dataset

# Carregar os dados
dados = pd.read_excel('Dados_Tratados.xlsx')

dados = dados.dropna()

# Converter MesReferencia para tipo datetime
dados['MesReferencia'] = pd.to_datetime(dados['MesReferencia'])

# Agrupar os dados por Marca e Modelo e criar uma série temporal para cada grupo
dados_agrupados = dados.groupby('Modelo')

# Calcular a média do valor para cada modelo
media_por_modelo = dados_agrupados['Valor'].mean()

# Selecionar os modelos com média inferior a 70000
modelos_menos_de_70000 = media_por_modelo[media_por_modelo < 60000].index

# Filtrar os dados originais para incluir apenas os modelos selecionados
dados_selecionados = dados[dados['Modelo'].isin(modelos_menos_de_70000)]

series_temporais = {}
for grupo, dados_grupo in dados_selecionados.groupby('Modelo'):
    # Ordenar os dados pelo MesReferencia
    dados_grupo = dados_grupo.sort_values('MesReferencia')
    
    # Extrair os valores da característica de interesse (por exemplo, Valor)
    valores = dados_grupo['Valor'].values
    
    # Extrair os índices de tempo (MesReferencia)
    indices_temporais = dados_grupo['MesReferencia'].values
    
    # Criar a série temporal
    serie_temporal = pd.Series(data=valores, index=indices_temporais)
    
    # Adicionar a série temporal à lista de séries temporais
    series_temporais[grupo] = serie_temporal

dados_series_temporais = to_time_series_dataset(list(series_temporais.values()))

# Definir o número de clusters desejado
num_clusters = 9

# Criar o modelo TimeSeriesKMeans
modelo_kmeans = TimeSeriesKMeans(n_clusters=num_clusters, metric="dtw", verbose=True, max_iter_barycenter=10, random_state=42, n_jobs=-1)

# Ajustar o modelo aos dados
modelo_kmeans.fit(dados_series_temporais)
print('Treinamento Finalizado')

# Prever os clusters para as séries temporais
rotulos_clusters = modelo_kmeans.predict(dados_series_temporais)

# Configurações de plotagem
plt.figure(figsize=(15, 10))

# Plotar a série temporal para cada cluster
for yi in range(num_clusters):
    plt.subplot(3, 3, yi + 1)
    for xx in dados_series_temporais[rotulos_clusters == yi]:
        plt.plot(xx.ravel(), "k-", alpha=.2)
    plt.plot(modelo_kmeans.cluster_centers_[yi].ravel(), "r-")
    plt.text(0.55, 0.85,'Cluster %d' % (yi),
             transform=plt.gca().transAxes)
    if yi == 1:
        plt.title("DBA $k$-means")

plt.tight_layout()
plt.show()

# Mostrar os modelos alocados em cada grupo
for cluster in range(num_clusters):
    print(f"Grupo {cluster}:")
    for modelo, serie_temporal in series_temporais.items():
        if rotulos_clusters[list(series_temporais.keys()).index(modelo)] == cluster:
            print(modelo)
    print("\n")

# Criar um dicionário para mapear os modelos aos clusters
modelo_cluster_map = {}
for modelo, serie_temporal in series_temporais.items():
    modelo_cluster_map[modelo] = rotulos_clusters[list(series_temporais.keys()).index(modelo)]

# Adicionar a coluna 'Cluster' ao DataFrame
dados_selecionados['Cluster'] = dados_selecionados['Modelo'].map(modelo_cluster_map)

# Verificar o DataFrame modificado
print(dados_selecionados.head())

# Salvar o DataFrame modificado como um arquivo Excel
dados_selecionados.to_excel('Dados_Clusterizados.xlsx', index=False)