# script focado em ler os dados do banco e fazer a análise
#importando as bibliotecas  apara leitura e visualização de dados 
import pandas as pd
import sqlite3  
import matplotlib.pyplot as plt 
import seaborn as sns 
import matplotlib.dates as mdates



print("Analisando os dados de produção...")
# esse comando conecta o banco de dados (con)
con = sqlite3.connect('producao.db')

try:
    #função do pandas que lê o resultado de uma query SQL e transforma em um DataFrame
    # A consulta SQL 'SELECT * producao_maquinas '  le todos dados da tabela producao_maquinas
    df = pd.read_sql_query("SELECT * FROM producao_maquinas;", con)
    print("\n Dados carregados do banco de dados para um DataFrame Pandas: ")
    print(df)
    #-----1 Ver colunas e tipos de dados (df.info()) ----
    # Esse print vai mostrar o nome das colunas , a quantidade de valores nao nulos e o tipo de dado de cada coluna.
    print("\n --Informações do DataFrame--(df.info())---")
    df.info()
    
    #--------Limpeza e tratamento dos dados 
    # remover a linha onde a coluna "data é nula"
    df.dropna(subset=['data'], inplace=True) 

   
    #formato data hora
    df['data'] = pd.to_datetime(df['data'], errors='coerce')
    #Isso converte automaticamente e coloca NaT em valores inválidos, evitando quebra.
    


  
    # Preenchendo valores ausentes com a média para não distorcer a análise"

    df['horas_trabalhadas'] = df['horas_trabalhadas'].fillna(df['horas_trabalhadas'].mean())
    df['falhas'] = df['falhas'].fillna(df['falhas'].mean())
    df['producao'] = df['producao'].fillna(df['producao'].mean())

    #falha encontrada e corrigifa  antes a linha poderia quebrar se restase algum NaN
    df['falhas'] = df['falhas'].fillna(0).astype(int)

    # Criando uma nova métrica #Taxa de Falha por Hora
    df['falhas_por_hora'] = df['falhas'] / df['horas_trabalhadas']

    #verificando o resultado do tratamento 
    print("\n---Informações do DataFrame após o tratamento dos dados ---'")
    df.info()
    

    #verificando o resultado do tratamento 
    print("\n---Estatísticas descritivas do DataFrame após o tratamento dos dados")
    print(df.describe())

    #----------Fim da etapa de limpeza e tratamento de dados para insight preciso qualidade dos dados é importante para o tipo de analise e tomar a melhor decisão
    #-------------------

    #------ Visualização dos grafica dados 
    # 1. agrupando os dados e somando as falhas por maquina 
    falhas_por_maquina = df.groupby('maquina')['falhas']. sum().sort_values(ascending = False)
    # 2-Configurando o tamanho da figura 
    plt.figure(figsize=(10, 6))
    # 3-criando  o grafico de barras 
    sns.barplot(x=falhas_por_maquina.index, y=falhas_por_maquina.values, palette='viridis')
    # 4 . adicionando titulos e rotulos para clareza 
    plt.title('Total de falhas por maquina',fontsize=16)
    plt.xlabel('Maquina', fontsize=12)
    plt.ylabel('Numero total de Falhas', fontsize=12)
    #5.Este é o comando que renderiza e exibe o gráfico
    plt.show()
    #-----fim da  visualizaçao grafica-------

    # Criando um gráfico de linha para visualizar a produção ao longo do tempo
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df, x='data', y='producao', hue='maquina', marker='o')

    # CORRIGIDO: Adicionando o rótulo correto para o eixo X
    plt.xlabel('Data', fontsize=12)
    plt.ylabel('Produção', fontsize=12)

    # NOVO: Formatando o eixo X para mostrar apenas a data
    # O formatador de data usa o formato 'Mês-Dia'
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.xticks(rotation=45)

    plt.title('Produção de Máquinas ao Longo do Tempo', fontsize=16)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    # --DEIXANDO O CODIGO MAIS ROBUSTO----
    # encontrando a maquina com melhor desempenho de forma automática e inteligente
    # 1. Encontrando a máquina com o melhor desempenho
    maquina_melhor_desempenho = df.loc[df['producao'].idxmax()]

    # 2. Extraindo o valor e a data do melhor desempenho
    melhor = df.loc[df['producao'].idxmax()]
    maquina_melhor_desempenho = melhor['maquina']
    valor_melhor_desempenho = melhor['producao']
    data_melhor_desempenho = melhor['data']

    plt.annotate(
        f'Melhor desempenho: {maquina_melhor_desempenho} ({data_melhor_desempenho.strftime("%Y-%m-%d")})',
        xy=(data_melhor_desempenho, valor_melhor_desempenho),
        xytext=(data_melhor_desempenho, valor_melhor_desempenho + 5),
        arrowprops=dict(facecolor='black', shrink=0.05),
        fontsize=10,
        bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=1, alpha=0.5)
    )

    plt.show()
    #----fim grafico de linha -produçao ao longo do tempo--------------
    
    # --DEIXANDO O CODIGO MAIS ROBUSTO----
    # encontrando a maquina com melhor desempenho de forma automática e inteligente 
    # 1. Encontrando a máquina com o melhor desempenho
    # Usamos idxmax() para encontrar o índice (nome da máquina) da maior produção
    maquina_melhor_desempenho = df['producao'].idxmax()

    # 2. Encontrando os dados de produção dessa máquina
    # loc localiza a linha da máquina com o melhor desempenho
    dados_melhor_desempenho = df.loc[df['maquina'] == maquina_melhor_desempenho]

    # 3. Extraindo o valor e a data do melhor desempenho
    # Usamos.max() e.dt.strftime() para pegar o valor e formatar a data
    valor_melhor_desempenho = dados_melhor_desempenho['producao'].max()
    data_melhor_desempenho = dados_melhor_desempenho['data'].max().strftime('%Y-%m-%d')


    # 4. Criando o texto da anotação de forma automática
    # O texto é construído com os dados que o código encontrou
    texto_anotacao = f'Melhor desempenho: {maquina_melhor_desempenho} ({data_melhor_desempenho})'

    # 5. Adicionando a anotação dinâmica ao gráfico
    plt.annotate(
    texto_anotacao,
    xy=(data_melhor_desempenho, valor_melhor_desempenho),  # Ponto do dado a ser anotado
    xytext=(1.1, 1.05),  # Posição do texto (valores ajustáveis)
    xycoords='axes fraction',
    fontsize=10,
    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=1, alpha=0.5))  #Adiciona uma caixa de fundo




    #----  estatisticas BASICAS 
    # Esse print vai mostrar estatísticas descritivas básicas para colunas numéricas, como contagem, média, desvio padrão, valores mínimos e máximos, e os quartis.
    print("\n--- Contagem de falhas por máquina ---")
    falhas_por_maquina = df.groupby('maquina')['falhas'].sum()
    print(falhas_por_maquina)
    print("\n--- Produção média por máquina ---")
    producao_media_por_maquina = df.groupby('maquina')['producao'].mean()
    print(producao_media_por_maquina)
    #----- fim das estatisticas -------

#Inicio do tratamento de erros 
except Exception as e:
    print(f"Erro ao carregar dados do banco de dados: {e}")
    print("Certifique-se de que o banco de dados e a tabela existem e estão acessíveis.")

finally:
    # Fechando a conexão com o banco de dados
    con.close()
    print("Análise concluída. Conexão com o banco de dados fechada.")







