📊 Análise de Dados Industriais com Python

🔍 Projeto de análise exploratória de métricas de desempenho de máquinas, com foco em identificar padrões de falhas e otimizar a produção.

Este repositório demonstra meu processo de trabalho em Ciência de Dados aplicada ao contexto industrial, desde a preparação dos dados até a geração de insights e visualizações.

🎯 Objetivos do Projeto

Identificar e Correlacionar Variáveis → entender a relação entre horas trabalhadas, número de falhas e volume de produção.

Prever Falhas → analisar padrões de falhas para antecipar problemas e reduzir custos de manutenção.

Otimizar a Produção → criar visualizações que auxiliam decisões estratégicas e aumentam eficiência operacional.

🛠️ Tecnologias e Metodologia

Linguagem: Python 🐍

Análise e Manipulação de Dados: Pandas

Banco de Dados: SQLite + sqlite3

Visualização de Dados: Matplotlib & Seaborn

Versionamento: Git & GitHub

📌 Metodologia → fluxo completo de análise de dados: ingestão → tratamento → análise → visualização → insights.

📂 Estrutura do Projeto
.
├── producao.db      # Banco de dados SQLite com dados brutos
├── producao.ods     # Dataset original em planilha
├── producao.py      # Script para criar e popular a tabela
└── analise.py       # Script principal com análise e gráficos

📈 Análises e Insights

Preparação e Limpeza de Dados → tratamento de valores ausentes e padronização.

Estatísticas Descritivas → contagem de falhas, médias de produção por máquina, agrupamentos.

Visualizações Criadas:

📊 Total de falhas por máquina → identificar equipamentos críticos.

📈 Produção ao longo do tempo → acompanhar evolução e desempenho.

🚀 Próximos Passos

🔮 Análise Preditiva → aplicar Machine Learning para prever falhas.

📊 Dashboard Interativo → desenvolver visualização dinâmica com Plotly/Streamlit.

⚙️ Automação → criar pipeline para atualização contínua dos dados.

▶️ Como Usar

Clone o repositório:
git clone https://https://github.com/marco-dev-pinheiro/analise-dados-industriais

Instale as dependências:

pip install pandas matplotlib seaborn sqlalchemy

Crie o banco de dados:
python producao.py

Rode a análise e gere os gráficos:
python analise.py

💡 Por que este projeto é relevante?

Este projeto mostra como dados industriais podem gerar valor real:

Redução de custos com manutenção preditiva.

Aumento da eficiência produtiva.

Suporte a decisões estratégicas baseadas em dados.



