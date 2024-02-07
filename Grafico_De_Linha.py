import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do arquivo Excel
data = pd.read_excel('Dados Tabela Fipe.xlsx')
data['Valor'] = data['Valor'].apply(lambda x: (int(str(x).split("R$ ")[1].replace('.','').split(',')[0])))

# Agrupar por marca
grouped_data = data.groupby('Marca')

diferenca = input('Você quer a diferença do preço?')

# Plotar o gráfico
plt.figure(figsize=(12, 6))  # Definir o tamanho da figura

# Iterar sobre cada grupo (marca)
for marca, grupo in grouped_data:
    # Iterar sobre cada modelo dentro do grupo
    for modelo in grupo['Modelo'].unique():
        modelo_data = grupo[grupo['Modelo'] == modelo]
        # diferença de valores dos preços por modelo
        if diferenca.lower() in ['y', 's', 'sim', 'yes']:
            diff_values = modelo_data['Valor'].diff().dropna()
            plt.plot(modelo_data['MesReferencia'].iloc[1:], diff_values, label=modelo + ' - ' + marca)
        else:
            plt.plot(modelo_data['MesReferencia'], modelo_data['Valor'], label=modelo + ' - ' + marca)

    # Adicionar rótulos aos eixos e título ao gráfico
    plt.xlabel('Mês de Referência')
    plt.ylabel('Valor')
    plt.title('Valores por Mês de Referência para cada Modelo e Marca')
    plt.xticks(rotation=45)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)  # Adicionar grade para melhor visualização
    plt.tight_layout()  # Ajustar layout para melhor visualização dos elementos
    plt.show()