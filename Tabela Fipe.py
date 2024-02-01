import pandas as pd
import re
from pyfipe.core import ConsultaFipe
from pyfipe.tabelas import consulta_tabela_referencia, consulta_tabela_marcas, consulta_tabela_modelos

# Lista para armazenar todos os DataFrames de preços
lista_dfs_precos = []

df_final = pd.read_excel("Dados Tabela Fipe.xlsx")
ultima_linha = df_final.iloc[-1]

# Extraindo o mês, a marca e o modelo da última linha
ultimo_mes = ultima_linha['MesReferencia']
ultima_marca = ultima_linha['Marca']
ultimo_mes = re.sub(r'\s+de\s+', '/', str(ultimo_mes)).split()[0]

# Removendo meses mais recentes do que o último mês na planilha
meses_disponiveis = list(reversed(consulta_tabela_referencia()['mes']))
meses_para_consultar = meses_disponiveis[:meses_disponiveis.index(ultimo_mes) - 1]
#Iterando em todos os meses disponiveis
for mes in meses_para_consultar:
    print(mes)
    lista_marcas = consulta_tabela_marcas(mes=mes, tipo_veiculo='carro')
    #Iterando em todas as marcas do respectivo mes
    if ultima_marca in lista_marcas['marca'].values:
        indice_ultima_marca = list(lista_marcas['marca']).index(ultima_marca)
        marcas_para_consultar = lista_marcas['marca'].iloc[indice_ultima_marca:]
        #Iterando em todos os modelos da marca (provavelmente o problema está no mes x modelo)
        for marca in marcas_para_consultar:
            codigo_marca = lista_marcas.loc[lista_marcas['marca'] == marca, 'codigo_marca'].iloc[0]
            modelos_marca = consulta_tabela_modelos(mes=mes, tipo_veiculo='carro', codigo_marca=codigo_marca)
            
            # Lista para armazenar as primeiras palavras dos modelos
            primeiras_palavras = []

            # Filtrando os modelos para retirar modelos parecidos
            # Estou removendo os que contem a primeira palavra igual
            modelos_filtrados = []
            for modelo in modelos_marca['modelo']:
                primeira_palavra = re.split(r'\s|-', modelo)[0].lower()
                if primeira_palavra not in primeiras_palavras:
                    primeiras_palavras.append(primeira_palavra)
                    modelos_filtrados.append(modelo)

            for modelo in modelos_filtrados:
                if modelo in df_final['Modelo'].values:
                    ano_modelo = df_final.loc[df_final['Modelo'] == modelo, 'AnoModelo'].iloc[0]
                else:
                    ano_modelo = int(str(mes).split('/')[1])-1
                print(f'mes: {mes}\nmarca: {marca}\nmodelo: {modelo}\nano modelo: {ano_modelo}')
                preco = ConsultaFipe(
                    mes=str(mes),
                    tipo_veiculo='carro',
                    marca=str(marca),
                    modelo=str(modelo),
                    ano_modelo=ano_modelo
                ).preco()
                
                if not ('erro' in preco.columns):
                    print(preco)
                    lista_dfs_precos.append(preco)

                else:
                    print("Erro! Modelo não encontrado!")

            # Adicionando a primeira palavra vista ao conjunto
            df_final = pd.concat(lista_dfs_precos)
            df_final.to_excel("Dados Tabela Fipe.xlsx", index=False)