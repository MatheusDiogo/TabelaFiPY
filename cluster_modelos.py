import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Carregar os dados
dados = pd.read_excel('Dados_Tratados.xlsx')

# Selecionar as características para o modelo
caracteristicas = ['Valor', 'Classificacao_Marca', 'Classificacao_Modelo', 'Idade_modelo']

# Normalizar os dados
scaler = StandardScaler()
dados[caracteristicas] = scaler.fit_transform(dados[caracteristicas])

# Escolher o número de clusters
n_clusters = 5

# Aplicar o algoritmo de clustering
kmeans = KMeans(n_clusters=n_clusters)
dados['Cluster'] = kmeans.fit_predict(dados[caracteristicas])

# Mostrar as marcas alocadas em cada grupo
for cluster in range(n_clusters):
    print(f"Grupo {cluster}:")
    print(dados[dados['Cluster'] == cluster]['Marca'].value_counts())
    print("\n")

# Visualização dos clusters
fig, axs = plt.subplots(1, 2, figsize=(16, 6))

for cluster in range(n_clusters):
    dados_cluster = dados[dados['Cluster'] == cluster]
    axs[0].scatter(dados_cluster['Idade_modelo'], dados_cluster['Valor'], label=f'Cluster {cluster}')
axs[0].set_title('Valor vs Idade - Clusters de Modelos de Carro')
axs[0].set_xlabel('Idade')
axs[0].set_ylabel('Valor')
axs[0].legend()

# Boxplot dos clusters
axs[1].boxplot([dados[dados['Cluster'] == cluster]['Valor'] for cluster in range(n_clusters)], patch_artist=True)
axs[1].set_title('Boxplot dos Clusters')
axs[1].set_xlabel('Cluster')
axs[1].set_ylabel('Valor')
axs[1].set_xticks(range(1, n_clusters + 1), [f'Cluster {i}' for i in range(n_clusters)])
axs[1].grid(True)

plt.tight_layout()
plt.show()