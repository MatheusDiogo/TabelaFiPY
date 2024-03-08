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
dados_agrupados = dados.groupby(['Marca', 'Modelo'])

series_temporais = []
for grupo, dados_grupo in dados_agrupados:
    # Ordenar os dados pelo MesReferencia
    dados_grupo = dados_grupo.sort_values('MesReferencia')
    
    # Extrair os valores da característica de interesse (por exemplo, Valor)
    valores = dados_grupo['Valor'].values
    
    # Extrair os índices de tempo (MesReferencia)
    indices_temporais = dados_grupo['MesReferencia'].values
    
    # Criar a série temporal
    serie_temporal = pd.Series(data=valores, index=indices_temporais)
    
    # Adicionar a série temporal à lista de séries temporais
    series_temporais.append(serie_temporal)

dados_series_temporais = to_time_series_dataset(series_temporais)

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

# Plotar cada série temporal com cores diferentes para cada cluster
for yi in range(num_clusters):
    plt.subplot(3, 3, yi + 1)
    for xx in dados_series_temporais[rotulos_clusters == yi]:
        plt.plot(xx.ravel(), "k-", alpha=.2)
    plt.plot(modelo_kmeans.cluster_centers_[yi].ravel(), "r-")
    plt.text(0.55, 0.85,'Cluster %d' % (yi + 1),
             transform=plt.gca().transAxes)
    if yi == 1:
        plt.title("DBA $k$-means")

plt.tight_layout()
plt.show()
# # Selecionar as características para o modelo
# caracteristicas = ['Classificacao_Modelo', 'Valor', 'AnoModelo','Idade_modelo', 'Inflacao_Total', 'Inflacao_Mensal', 'Inflacao_Trimestral', 'Inflacao_Semestral', 'Inflacao_Anual']

# # Normalizar os dados
# scaler = StandardScaler()
# dados[caracteristicas] = scaler.fit_transform(dados[caracteristicas])

# # Converter os dados para séries temporais
# dados_series_temporais = to_time_series_dataset(dados[caracteristicas])

# # Escolher o número de clusters
# n_clusters = 5

# # Aplicar o algoritmo de clustering
# kmeans = TimeSeriesKMeans(n_clusters=n_clusters, metric='euclidean', random_state=42)
# dados['Cluster'] = kmeans.fit_predict(dados_series_temporais)

# # Mostrar as marcas alocadas em cada grupo
# for cluster in range(n_clusters):
#     print(f"Grupo {cluster}:")
#     print(dados[dados['Cluster'] == cluster]['Marca'].value_counts())
#     print("\n")

# # Visualização dos clusters
# fig, axs = plt.subplots(1, 2, figsize=(16, 6))

# for cluster in range(n_clusters):
#     dados_cluster = dados[dados['Cluster'] == cluster]
#     axs[0].scatter(dados_cluster['Idade_modelo'], dados_cluster['Valor'], label=f'Cluster {cluster}')
# axs[0].set_title('Valor vs Idade - Clusters de Modelos de Carro')
# axs[0].set_xlabel('Idade')
# axs[0].set_ylabel('Valor')
# axs[0].legend()

# # Boxplot dos clusters
# axs[1].boxplot([dados[dados['Cluster'] == cluster]['Valor'] for cluster in range(n_clusters)], patch_artist=True)
# axs[1].set_title('Boxplot dos Clusters')
# axs[1].set_xlabel('Cluster')
# axs[1].set_ylabel('Valor')
# axs[1].set_xticks(range(1, n_clusters + 1), [f'Cluster {i}' for i in range(n_clusters)])
# axs[1].grid(True)

# plt.tight_layout()
# plt.show()

# dados[caracteristicas] = scaler.inverse_transform(dados[caracteristicas])

# dados.to_excel('Dados_Clusterizados.xlsx', index = False)