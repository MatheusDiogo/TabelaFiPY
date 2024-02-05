import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import normaltest

# Função para converter mês por extenso para número do mês
def mes_para_numero(mes_extenso):
    meses = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6,
        'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }
    mes, ano = mes_extenso.lower().split(" de ")
    return pd.Timestamp(year=int(ano), month=meses[mes], day=1)

# Carregar dados
data = pd.read_excel('Dados Tabela Fipe.xlsx')

# Converter a coluna 'MesReferencia' para o formato de data
data['MesReferencia'] = data['MesReferencia'].apply(mes_para_numero)

# Formatar valor do carro
data['Valor'] = data['Valor'].apply(lambda x: (int(str(x).split("R$ ")[1].replace('.','').split(',')[0])))

# Calcular a diferença de valores dos preços dos carros
data['Diff_Valor'] = data.groupby(['Marca', 'Modelo'])['Valor'].diff()

# Plotar o gráfico
plt.figure(figsize=(12, 6))

# Plotar o histograma das diferenças de valores
plt.subplot(1, 2, 1)
data['Diff_Valor'].hist(bins=50)
plt.title('Histograma das Diferenças de Valores dos Carros')
plt.xlabel('Diferença de Valor')
plt.ylabel('Frequência')
plt.grid(True)

# Plotar o boxplot das diferenças de valores
plt.subplot(1, 2, 2)
data.boxplot(column='Diff_Valor')
plt.title('Boxplot das Diferenças de Valores dos Carros')
plt.ylabel('Diferença de Valor')
plt.grid(True)
plt.show()

# Filtrar outliers (considerando valores além de 3 desvios padrão da média como outliers)
mean_diff = data['Diff_Valor'].mean()
std_diff = data['Diff_Valor'].std()
data_filtrado = data[(data['Diff_Valor'] >= mean_diff - 2*std_diff) & (data['Diff_Valor'] <= mean_diff + 2*std_diff)]

# Plotar o gráfico com os outliers removidos
plt.figure(figsize=(12, 6))

# Plotar o histograma das diferenças de valores
plt.subplot(1, 2, 1)
data_filtrado['Diff_Valor'].hist(bins=50)
plt.title('Histograma das Diferenças de Valores dos Carros')
plt.xlabel('Diferença de Valor')
plt.ylabel('Frequência')
plt.grid(True)

# Plotar o boxplot das diferenças de valores
plt.subplot(1, 2, 2)
data_filtrado.boxplot(column='Diff_Valor', showfliers=False)
plt.title('Boxplot das Diferenças de Valores dos Carros')
plt.ylabel('Diferença de Valor')
plt.grid(True)
plt.show()

stat_test, p_valor = normaltest(data_filtrado.Diff_Valor)
print(stat_test)
print(p_valor)