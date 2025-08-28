# script focado em ler os dados do banco e fazer a análise
import pandas as pd
import sqlite3  

print("Analisando os dados de produção...")
# esse comando conecta o banco de dados (con)
con = sqlite3.connect('producao.db')

try:
    #função do pandas que lê o resultado de uma query SQL e transforma em um DataFrame
    # A consulta SQL 'SELECT * producao_maquinas '  le todos dados da tabela producao_maquinas
    df = pd.read_sql_query("SELECT * FROM producao_maquinas;", con)
    print("\n Dados carregados do banco de daods para um DataFrame Pandas: ")
    print(df)
    #-----1 Ver colunas e tipos de dados (df.info()) ----
    # Esse print vai mostrar o nome das colunas , a quantidade de valores nao nulos e o tipo de dado de cada coluna.
    print("\n --Informações do DataFrame--(df.info())---")
    df.info()

    #---- 2 estatisticas BASICAS (df.describe()) ----
    # Esse print vai mostrar estatísticas descritivas básicas para colunas numéricas, como contagem, média, desvio padrão, valores mínimos e máximos, e os quartis.
    print("\n ---Estatísticas descritivas do DataFrame (df.describe())---")
    print(df.describe())

    print("n--- Contagem de falhas por máquina ---")
    falhas_por_maquina = df.groupby('maquina')['falhas'].sum()
    print(falhas_por_maquina)
    print("\n--- Produção média por máquina ---")
    producao_media_por_maquina = df.groupby('maquina')['producao'].mean()
    print(producao_media_por_maquina)
except Exception as e:
    print(f"Erro ao carregar dados do banco de dados: {e}")
    print("Certifique-se de que o banco de dados e a tabela existem e estão acessíveis.")

finally:
    # Fechando a conexão com o banco de dados
    con.close()
    print("Análise concluída. Conexão com o banco de dados fechada.")







