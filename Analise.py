import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do arquivo Excel
data = pd.read_excel('Dados Tabela Fipe.xlsx')

# Agrupar por marca
grouped_data = data.groupby('Marca')

# Plotar o gráfico
plt.figure(figsize=(10, 6))  # Definir o tamanho da figura

# Iterar sobre cada grupo (marca)
for marca, grupo in grouped_data:
    # Iterar sobre cada modelo dentro do grupo
    for modelo in grupo['Modelo'].unique():
        modelo_data = grupo[grupo['Modelo'] == modelo]
        plt.plot(modelo_data['MesReferencia'], modelo_data['Valor'], label=modelo + ' - ' + marca)

    # Adicionar rótulos aos eixos e título ao gráfico
    plt.xlabel('Mês de Referência')
    plt.ylabel('Valor')
    plt.title('Valores por Mês de Referência para cada Modelo e Marca')
    plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo X para facilitar a leitura
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Adicionar legenda fora do gráfico
    plt.grid(True)  # Adicionar grade para melhor visualização
    plt.tight_layout()  # Ajustar layout para melhor visualização dos elementos
    plt.show()