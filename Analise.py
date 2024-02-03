import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do arquivo Excel
data = pd.read_excel('Dados Tabela Fipe.xlsx')
data['Valor'] = data['Valor'].apply(lambda x: (int(str(x).split("R$ ")[1].replace('.','').split(',')[0])))

# Agrupar por marca
grouped_data = data.groupby('Marca')

# Plotar o gráfico
plt.figure(figsize=(14, 8))  # Definir o tamanho da figura

# Iterar sobre cada grupo (marca)
for marca, grupo in grouped_data:
    # Iterar sobre cada modelo dentro do grupo
    for modelo in grupo['Modelo'].unique():
        modelo_data = grupo[grupo['Modelo'] == modelo]
        # diferença de valores dos preços por modelo
        diff_values = modelo_data['Valor'].diff().dropna()
        plt.plot(modelo_data['MesReferencia'].iloc[1:], diff_values, label=modelo + ' - ' + marca)

    # Adicionar rótulos aos eixos e título ao gráfico
    plt.xlabel('Mês de Referência')
    plt.ylabel('Valor')
    plt.title('Valores por Mês de Referência para cada Modelo e Marca')
    plt.xticks(rotation=45)  # Rotacionar os rótulos do eixo X para facilitar a leitura
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Adicionar legenda fora do gráfico
    plt.grid(True)  # Adicionar grade para melhor visualização
    plt.tight_layout()  # Ajustar layout para melhor visualização dos elementos
    plt.show()