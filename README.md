# 📊 Dashboard de Análise de Produção Industrial

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)  
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange?logo=pandas)  
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-9cf?logo=plotly)  
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite)  
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-ff4b4b?logo=streamlit)  
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)  
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Sobre o Projeto
Este projeto simula e analisa a **produção industrial** de diferentes máquinas, integrando um pipeline **ETL → Banco de Dados → Dashboard**.  

O objetivo é demonstrar como **dados industriais** podem ser gerados, tratados, armazenados em **SQLite** e visualizados em um **dashboard interativo com Streamlit**.  

🔎 Ideal para estudos de **engenharia de dados**, **análise estatística** e **visualização de KPIs industriais**.

---

## 🎯 Objetivos
- Gerar dados industriais **realistas** (produção, falhas, horários de funcionamento).  
- Tratar e armazenar dados em um **banco relacional SQLite**.  
- Criar análises estatísticas e **gráficos interativos**.  
- Disponibilizar tudo em um **dashboard web intuitivo** com Streamlit.  

---

## 🛠️ Tecnologias Utilizadas
- 🐍 **Python 3.10+**
- 📦 **Pandas, Numpy**
- 📊 **Matplotlib, Seaborn**
- 🗄️ **SQLite**
- 🚀 **Streamlit**
- 🔧 **ETL Pipeline**

---

## 🗂️ Estrutura do Projeto

```bash
📦 projeto-analise-industrial
├── 📂 src
│   ├── generate_data.py      # Gera dados simulados de produção
│   ├── producao.py           # ETL → trata dados e salva no SQLite
│   ├── analise.py            # Funções de análise e gráficos
│   ├── app_streamlit.py      # Dashboard interativo
│
├── 📂 data
│   ├── 📂 raw                # Dados brutos
│   │   └── producao_raw.csv
│   ├── 📂 processed          # Dados tratados
│   │   └── producao.db       # Banco SQLite
│
├── 📂 reports
│   ├── img/                  # Imagens e gráficos para o README
│   │   └── <!-- adicione aqui -->
│
├── requirements.txt          # Dependências do projeto
└── README.md                 # Documentação

#    Fluxo de Dados (ETL → Análise → Dashboard)

flowchart LR
    A[📄 generate_data.py] -->
    A --> B[🛠️ producao.py (ETL)]
    B --> C[(🗄️ SQLite: producao.db)]
    C --> D[📊 analise.py]
    D --> E[🚀 app_streamlit.py (Dashboard)]




## Instalação

# ▶️ Como Executar o Projeto

## 1️⃣ Clonar o Repositório
 git clone https://github.com/seu-usuario/    projeto-analise-industrial.git
cd projeto-analise-industrial

2️⃣ Criar e Ativar o Ambiente Virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

3️⃣ Instalar Dependências
pip install -r requirements.txt

4️⃣ Executar o Pipeline ETL
python src/generate_data.py
python src/producao.py

5️⃣ Rodar o Dashboard
streamlit run src/app_streamlit.py





###🚀 Próximos Passos

[] Exportação de relatórios automáticos em PDF/Excel

[] Deploy do Streamlit na nuvem (Streamlit Cloud / Heroku)

[] Integração com dados em tempo real
## Autores

## 📸 Demonstração

![Dashboard](reports/img/dashboard.png)
![Gráfico de Produção](reports/img/producao.png)
![Análise de Falhas](reports/img/falhas.png)
![Produção Mensal](reports/img/mensalproducao.png)
![Tabela de resumo](reports/img/tabelaresumo.png)
![Previsão de produção](reports/img/previsao.png)




[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/marco-pinheiro-34256b373/)


