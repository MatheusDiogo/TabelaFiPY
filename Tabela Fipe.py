import pandas as pd
import re
from pyfipe.core import ConsultaFipe
from pyfipe.tabelas import consulta_tabela_referencia, consulta_tabela_marcas, consulta_tabela_modelos

def main():
    print("Iniciando...")
    df_final = pd.read_excel("Dados Tabela Fipe.xlsx")
    ultima_linha = df_final.iloc[-1]

    # Extraindo o mês, a marca e o modelo da última linha
    ultimo_mes = ultima_linha['MesReferencia']
    ultima_marca = ultima_linha['Marca']
    ultimo_mes = re.sub(r'\s+de\s+', '/', str(ultimo_mes)).split()[0]

    # Removendo meses mais recentes do que o último mês na planilha
    meses_disponiveis = list(reversed(consulta_tabela_referencia()['mes']))
    meses_para_consultar = meses_disponiveis[meses_disponiveis.index(ultimo_mes):]
    #Iterando em todos os meses disponiveis
    for mes in meses_para_consultar:
        lista_marcas = consulta_tabela_marcas(mes=str(mes), tipo_veiculo='carro')
        #Iterando em todas as marcas do respectivo mes
        if ultima_marca in lista_marcas['marca'].values and ultimo_mes == mes:
            indice_ultima_marca = list(lista_marcas['marca']).index(ultima_marca)
            marcas_para_consultar = lista_marcas['marca'].iloc[indice_ultima_marca:]
        else:
            marcas_para_consultar = lista_marcas['marca']

        #Iterando em todos os modelos da marca (provavelmente o problema está no mes x modelo)
        for marca in marcas_para_consultar:
            # Lista para armazenar todos os DataFrames de preços
            lista_dfs_precos = []

            codigo_marca = lista_marcas.loc[lista_marcas['marca'] == marca, 'codigo_marca'].iloc[0]
            modelos_marca = consulta_tabela_modelos(mes=str(mes), tipo_veiculo='carro', codigo_marca=codigo_marca)
                
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
                #Verificando se o modelo já foi extraido em outros meses para pegar seu mes, senão é o mes atual
                if modelo in df_final['Modelo'].values:
                    ano_modelo = df_final.loc[df_final['Modelo'] == modelo, 'AnoModelo'].iloc[0]
                elif modelo not in consulta_tabela_modelos(mes=meses_disponiveis[meses_disponiveis.index(ultimo_mes):][0], tipo_veiculo='carro', codigo_marca=codigo_marca)['modelo']:
                    ano_modelo = int(str(mes).split('/')[1])
                else:
                    continue
                
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
                    novos_dados = pd.concat(lista_dfs_precos)
                else:
                    continue
                
                # Concatenando os dados e salvando os novos
                df_final = pd.concat([df_final, novos_dados])
                df_final.to_excel("Dados Tabela Fipe.xlsx", index=False)
                
        ultimo_mes = ultimo_mes

while True:
    try:
        main()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        continue