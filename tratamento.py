import pandas as pd

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
    # Salário Minímo
salario_minimo = pd.read_excel('Salario Minimo.xlsx')
salario_minimo['Data'] = pd.to_datetime(salario_minimo['Data'], format='%d/%m/%Y')
    # Dados FIPE
data = pd.read_excel('Dados Tabela Fipe.xlsx')
    # Inflação
inflacao = pd.read_excel('Inflação.xlsx', skiprows=3, sheet_name='Tabela 2').iloc[:1, 1:]
    # Cotação Dolar
df = pd.read_csv("USD_BRL Dados Históricos.csv", delimiter=",")

# Converter a coluna "Data" para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'], format='%d.%m.%Y')

# Calcular o peso de cada semana em relação ao fim do mês
df['Peso'] = df['Data'].dt.day.max() - df['Data'].dt.day + 1

# Calcular a média mensal ponderada
df['Valor'] = df['Último'].str.replace(',', '.').astype(float)
df['Valor_Ponderado'] = df['Valor'] * df['Peso']
media_mensal_ponderada = df.groupby(df['Data'].dt.to_period('M'))['Valor_Ponderado'].sum() / df.groupby(df['Data'].dt.to_period('M'))['Peso'].sum()

# Converter a série em DataFrame
dolar_df = media_mensal_ponderada.reset_index()
dolar_df['Data'] = dolar_df['Data'].apply(lambda x: pd.to_datetime(str(x)+'-01'))
dolar_df.columns = ['Data', 'Media_Dolar']

# Transformando data
data_inflacao = inflacao.transpose().reset_index().rename(columns={'index': 'Data'}).rename(columns={0: 'Inflacao'})
data_inflacao['Data'] = pd.to_datetime(data_inflacao['Data'].apply(mes_para_numero))

# Converter a coluna 'MesReferencia' para o formato de data
data['MesReferencia'] = data['MesReferencia'].apply(mes_para_numero)

# Mesclar com o DataFrame principal
data = pd.merge(data, salario_minimo, left_on='MesReferencia', right_on='Data', how='left')
data = pd.merge(data, data_inflacao, on='Data', how='left')
data = pd.merge(data, dolar_df, on='Data', how='left')
data = data.drop(columns=['Data'])

# Formatar valor do carro
data['Valor'] = data['Valor'].apply(lambda x: (int(str(x).split("R$ ")[1].replace('.','').split(',')[0])))

# Calcular a média dos valores por marca
media_por_marca = data.groupby('Marca')['Valor'].mean().sort_values()

# Criar um dicionário para mapear as marcas para suas classificações
classificacao = {}
ranking = 1
for marca, media_valor in media_por_marca.items():
    classificacao[marca] = ranking
    ranking += 1

# Adicionar uma nova coluna de classificação ao DataFrame
data['Classificacao'] = data['Marca'].map(classificacao)

# Exibir o DataFrame ordenado pela classificação
data = data.sort_values(by='Classificacao')

# Ordenar o DataFrame pela coluna 'Modelo' e 'MesReferencia'
data_sorted = data.sort_values(by=['Modelo', 'MesReferencia'])

# Calcular a diferença entre 'MesReferencia' e a primeira ocorrência de cada modelo para obter a idade do modelo em meses
data['Idade_modelo'] = data_sorted.groupby('Modelo')['MesReferencia'].transform(lambda x: (x - x.iloc[0]).dt.days // 30)

data = data.drop(columns=['TipoVeiculo', 'Combustivel', 'CodigoFipe', 'Autenticacao', 'SiglaCombustivel'])

data.to_excel('Dados_Tratados.xlsx', index=False)