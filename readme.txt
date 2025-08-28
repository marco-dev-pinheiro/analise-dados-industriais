# projeto  Dashboard de Analise Industrial 

# Projeto de Análise Industrial

Este é um projeto de análise de dados industriais, focado em entender a relação entre o tempo de operação, falhas e a produção de máquinas. A análise é dividida em etapas, começando pela preparação do ambiente e do dataset.

## Sumário
1. [Objetivo do Projeto](#objetivo-do-projeto)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Dia 1: Preparação do Ambiente e Dataset](#dia-1-preparacao-do-ambiente-e-dataset)
    - [Pré-requisitos](#pré-requisitos)
    - [Dataset](#dataset)
    - [Processo Executado](#processo-executado)
4. [Próximos Passos](#próximos-passos)

================================================================
### 1. Objetivo do Projeto

O objetivo principal é realizar uma análise de dados sobre a operação de máquinas em um ambiente industrial. Usando Python e bibliotecas como Pandas, Matplotlib e Seaborn, exploraremos um dataset fictício para identificar padrões, correlacionar variáveis (horas trabalhadas, falhas, produção) e criar visualizações para extrair insights valiosos.
=========================================================================
### 2. Estrutura do Projeto

A estrutura de arquivos atual do projeto é a seguinte:
.
├─  conceitos            # Conceitos técnicos importantes para entender/ ler-analisar/construir/
├── producao.ods         # Planilha de dados brutos (LibreOffice Calc)
├── producao.db          # Banco de dados SQLite com os dados carregados
└── analise.py  
      # Script Python para carregar e processar o dataset
============================================================================
### 3.  Preparação do Ambiente e Dataset

A primeira etapa do projeto foi focada em garantir que o ambiente estivesse pronto e que o dataset fosse criado, limpo e carregável.

#### Pré-requisitos
Para executar o script, é necessário ter o Python instalado. As seguintes bibliotecas precisam ser instaladas:

```bash
pip install pandas matplotlib seaborn sqlalchemy psycopg2

--pandas: Para manipulação e análise de dados.

--matplotlib e seaborn: Para visualização de dados.

--sqlalchemy: Para trabalhar com o banco de dados.

psycopg2: (Opcional) Biblioteca para PostgreSQL, embora no momento o projeto utilize SQLite.
==========================================================================
Dataset
O dataset fictício foi criado com as seguintes colunas:usei o libreoffice

Maquina: Identificador da máquina (ex: 'A1', 'B2', etc.).

Data: Data da operação.

Horas_trabalhadas: Horas de funcionamento da máquina naquele dia.

Falhas: Número de falhas reportadas.

Producao: Unidades produzidas pela máquina.

O dataset foi inicialmente criado em uma planilha (producao.ods) e, em seguida, carregado em um banco de dados SQLite (producao.db) para facilitar a manipulação.

Processo Executado
O script dahanalise.py foi responsável por:

Conectar-se a um banco de dados SQLite.

Criar uma tabela chamada producao_maquinas com a estrutura definida.

Inserir os dados da planilha na tabela, utilizando um método de inserção em lote (executemany) para maior eficiência.

Exibir as primeiras linhas da tabela no terminal para confirmar que o carregamento foi bem-sucedido.
=================================================================
#####Agora carregando o arquivo para um DataFrame do Pandas 
[v] Carregar os dados do banco de dados para um DataFrame do Pandas.

[v] Realizar uma análise exploratória dos dados (.info(), .describe()).
   Realizamos uma analise exploratória  

[v] Criar visualizações básicas para entender a distribuição das variáveis e a correlação entre elas (ex: gráficos de dispersão, histogramas).

######## Próximos passos 
[]Limpeza e tratamento

[]Identificar e corrigir:

[]Valores nulos.

[]Tipos errados (df['Data'] = pd.to_datetime(df['Data'])).

[]Colunas desnecessárias.

[]Criar novas métricas se precisar, ex: Falhas_por_hora = Falhas / Horas_trabalhadas.

