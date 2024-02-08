import pandas as pd
import matplotlib.pyplot as plt

# Função para converter mês por extenso para número do mês
def mes_para_numero(mes_extenso):
    meses = {
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6,
        'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }
    try:
        mes, ano = mes_extenso.lower().split(" de ")
        return pd.Timestamp(year=int(ano), month=meses[mes], day=1)
    except:
        mes, ano = mes_extenso.lower().split(" ")
        return pd.Timestamp(year=int(ano), month=meses[mes], day=1)

# Carregar dados
salario_minimo = pd.read_excel('Salario Minimo.xlsx')
salario_minimo['Data'] = pd.to_datetime(salario_minimo['Data'], format='%d/%m/%Y')
data = pd.read_excel('Dados Tabela Fipe.xlsx')
inflacao = pd.read_excel('Inflação.xlsx', skiprows=3, sheet_name='Tabela 2').iloc[:1, 1:]
data_inflacao = inflacao.transpose().reset_index().rename(columns={'index': 'Data'}).rename(columns={0: 'Inflacao'})
data_inflacao['Data'] = pd.to_datetime(data_inflacao['Data'].apply(mes_para_numero))

# Converter a coluna 'MesReferencia' para o formato de data
data['MesReferencia'] = data['MesReferencia'].apply(mes_para_numero)

# Mesclar as duas tabelas com base na correspondência de mês e ano
data = pd.merge(data, salario_minimo, left_on=data['MesReferencia'].dt.to_period('M'), right_on=salario_minimo['Data'].dt.to_period('M'), how='left')
print(data_inflacao)
data = pd.merge(data, data_inflacao, on='Data', how='left')

# Formatar valor do carro
data['Valor'] = data['Valor'].apply(lambda x: (int(str(x).split("R$ ")[1].replace('.','').split(',')[0])))

# Agrupar por marca
grouped_data = data.groupby('Marca')

teste = input('Você quer visualizar qual teste de correlação?\n1: Salário Mínimo\n2:Inflação\n$')

# Plotar o gráfico
plt.figure(figsize=(14, 8))

if teste == '1':
    for marca, grupo in grouped_data:
        # Iterar sobre cada modelo dentro do grupo
        for modelo in grupo['Modelo'].unique():
            modelo_data = grupo[grupo['Modelo'] == modelo]
            # diferença de valores dos preços por modelo
            modelo_data['Diff_Valor'] = modelo_data['Valor'].diff().dropna()
            # Calcular a correlação entre o salário mínimo e o valor dos carros
            correlacao = modelo_data['Salario'].corr(modelo_data['Valor'])
            
            # Plotando 2 gráficos por modelo
            plt.subplot(1, 3, 1)
            # Histograma da diferença dos valores
            modelo_data['Diff_Valor'].hist(bins=50, alpha=0.5, label=modelo)
            plt.title(f'Histograma da Diferença entre Valores\nModelo: {modelo}')
            plt.xlabel('Valor dos Carros')
            plt.ylabel('Frequência')
            plt.grid(True)
            plt.legend()
            
            # Plotar o gráfico de dispersão
            plt.subplot(1, 3, 2)
            plt.scatter(data['Salario'], data['Valor'], alpha=0.5)
            plt.title(f'Correlação entre Salário Mínimo e Valor')
            plt.xlabel('Salário Mínimo')
            plt.ylabel('Valor dos Carros')
            plt.grid(True)
            plt.text(data['Salario'].min(), data['Valor'].max(), f'Correlação: {correlacao:.2f}', fontsize=12, ha='right')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Adicionar legenda fora do gráfico

            # Histograma dos valores dos carros
            plt.subplot(1, 3, 3)
            modelo_data['Valor'].hist(bins=50, alpha=0.5, label=modelo)
            plt.title(f'Histograma do Valor dos Carros\nModelo: {modelo}')
            plt.xlabel('Valor dos Carros')
            plt.ylabel('Frequência')
            plt.grid(True)
            plt.legend()
            plt.show()

elif teste == '2':
    for marca, grupo in grouped_data:
        # Iterar sobre cada modelo dentro do grupo
        for modelo in grupo['Modelo'].unique():
            modelo_data = grupo[grupo['Modelo'] == modelo]
            # diferença de valores dos preços por modelo
            modelo_data['Diff_Valor'] = modelo_data['Valor'].diff().dropna()
            # Calcular a correlação entre o salário mínimo e o valor dos carros
            correlacao = modelo_data['Inflacao'].corr(modelo_data['Valor'])
            
            # Plotando 2 gráficos por modelo
            plt.subplot(1, 3, 1)
            # Histograma da diferença dos valores
            modelo_data['Diff_Valor'].hist(bins=50, alpha=0.5, label=modelo)
            plt.title(f'Histograma da Diferença entre Valores\nModelo: {modelo}')
            plt.xlabel('Valor dos Carros')
            plt.ylabel('Frequência')
            plt.grid(True)
            plt.legend()
            
            # Plotar o gráfico de dispersão
            plt.subplot(1, 3, 2)
            plt.scatter(data['Inflacao'], data['Valor'], alpha=0.5)
            plt.title(f'Correlação entre Inflacao e Valor')
            plt.xlabel('Inflacao')
            plt.ylabel('Valor dos Carros')
            plt.grid(True)
            plt.text(data['Inflacao'].min(), data['Valor'].max(), f'Correlação: {correlacao:.2f}', fontsize=12, ha='right')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Adicionar legenda fora do gráfico

            # Histograma dos valores dos carros
            plt.subplot(1, 3, 3)
            modelo_data['Inflacao'].hist(bins=50, alpha=0.5, label=modelo)
            plt.title(f'Histograma do Valor dos Carros\nModelo: {modelo}')
            plt.xlabel('Valor dos Carros')
            plt.ylabel('Frequência')
            plt.grid(True)
            plt.legend()
            plt.show()
