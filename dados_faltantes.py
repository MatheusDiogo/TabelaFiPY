import pandas as pd
import re
from pyfipe.core import ConsultaFipe
from pyfipe.tabelas import consulta_tabela_referencia, consulta_tabela_marcas, consulta_tabela_modelos

def main():
    print("Iniciando...")
    # Extraindo dados da tabela
    df_final = pd.read_excel("Dados Tabela Fipe.xlsx")
    
    # Obter o penúltimo mês na tabela
    ultimo_mes = df_final['MesReferencia'].iloc[-2]
    print(ultimo_mes)
    # Verificar se há modelos sem dados no último mês
    modelos_sem_dados = []
    for modelo in df_final['Modelo'].unique():
        if df_final[(df_final['Modelo'] == modelo) & (df_final['MesReferencia'] == ultimo_mes)].empty:
            modelos_sem_dados.append(modelo)
    
    # Criar uma lista para armazenar os últimos dados de cada modelo
    ultimos_dados_modelos = []
    
    lista_dfs_precos = []
    print(len(modelos_sem_dados))
    
    # Percorrer a lista de modelos sem dados
    for modelo in modelos_sem_dados:
        # Filtrar o DataFrame para obter os últimos dados do modelo atual
        ultimos_dados = df_final[df_final['Modelo'] == modelo].iloc[-1]
        # Adicionar os últimos dados do modelo à lista
        ultimos_dados_modelos.append(ultimos_dados)

    # Converter a lista de dicionários em DataFrame
    df_ultimos_dados = pd.DataFrame(ultimos_dados_modelos)
    
    for index, rows in df_ultimos_dados.iterrows():
        ultimo_mes_modelo = rows['MesReferencia'].replace(" de ", "/").strip()

        meses_disponiveis = list(reversed(consulta_tabela_referencia()['mes']))

        # Encontrar o índice do último mês do modelo na lista de meses disponíveis
        indice_ultimo_mes = meses_disponiveis.index(ultimo_mes_modelo)
        
        # Remover todos os meses anteriores ao último mês do modelo
        meses_disponiveis = meses_disponiveis[indice_ultimo_mes:]

        for mes in meses_disponiveis:
            try:
                #Consultanzo preco do modelo
                preco = ConsultaFipe(
                    mes=str(mes),
                    tipo_veiculo='carro',
                    marca=str(rows['Marca']),
                    modelo=str(rows['Modelo']),
                    ano_modelo=str(rows['AnoModelo'])
                ).preco()

            except:
                continue

            #Caso não encontre o modelo retornara um df com erro na coluna
            if not ('erro' in preco.columns):
                print(preco[['Valor', 'Marca', 'Modelo', 'AnoModelo', 'MesReferencia']])
                lista_dfs_precos.append(preco)
                # Concatenando os dados e salvando os novos
                novos_dados = pd.concat(lista_dfs_precos)
            else:
                continue
            
        #Remove os duplicados desconsiderando DataConsulta
        df_final = pd.concat([df_final, novos_dados], ignore_index=True).drop_duplicates(subset=df_final.columns.difference(['DataConsulta']))
        df_final.to_excel("Dados Tabela Fipe.xlsx", index=False)

#Laço para evitar quebra por falha na conexão com o site. Pode-se interromper o Script com CTRL + C
while True:
    try:
        main()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        continue