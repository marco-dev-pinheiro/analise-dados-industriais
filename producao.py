import sqlite3
import pandas as pd 

# Conectando ao banco de dados. Use uma extensão .db para arquivos de banco de dados.
# Se o arquivo não existir, o SQLite criará um novo.
con = sqlite3.connect('producao.db')

# Criando um cursor para interagir com o banco de dados.
# A ponte que conecta 
cur = con.cursor()

# --- Etapa 1: Criar a Tabela ---
#adicionar try except é uma boa pratica esse bloco captura erros na leitura do arquivo e da uma mensagem util , é muito importante o  tratamento de erros nos nossos scripts
try:

    df = pd.read_excel('producao.ods' , engine='odf')
   
    df.columns = df.columns.str.lower()
    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d')
    df['data'] = df['data'].dt.strftime('%Y-%m-%d')

    print("Dados lidos com sucesso do arquivo 'producao.ods'.")
except FileNotFoundError:
    print("Erro :O arquivo 'producao.ods' não foi encontrado. Verifique o caminho e tente novamente.")
    con.close() #fechando a conexao com o banco de dados.
    exit() #isso vai interromper o script se o arquivo n for encontrado


# --- Etapa 2: Inserir Dados ---

CREAT_TABLE_SQL="""
CREATE TABLE IF NOT EXISTS producao_maquinas (maquina VARCHAR(50) , data DATE , horas_trabalhadas FLOAT ,  falhas INT ,producao FLOAT );"""
#garantindo que a tabela n exista antes de criar
cur.execute(CREAT_TABLE_SQL) #criando a tabela
print ("Tabela 'producao_maquinas' criada ou já existe.")
#-------ETAPA 3: Preparar os Dados ------

dados = list(df .itertuples (index=False , name=None)) #convertendo o DataFrame para uma lista de tuplas
print(f"Dados convertidos para lista de tuplas. Total de registros: {len(dados)} linhas prontas para inserção.")
#-------ETAPA 4: Inserir os Dados ------
# Inserir os dados na tabela
#usando executemany para inserir todos os dados de uma vez

INSERT_DATA_SQL = "INSERT INTO producao_maquinas (maquina, data, horas_trabalhadas, falhas, producao) VALUES (?, ?, ?, ?, ?);"
#usando executemany para inserir todos os dados de uma vez
cur.executemany(INSERT_DATA_SQL, dados)#-------ETAPA 5 : Salvar e Fechar --
con.commit() #salvando as alterações
print(f"{cur.rowcount} registros inseridos na tabela 'producao_maquinas'.")
con.close() #fechando a conexão
print("Conexão com o banco de dados fechada.")


