"""
Módulo de análise e visualização para o dashboard.
Lê o banco SQLite, trata os dados, cria agregações e figuras.
Inclui prints/logging para acompanhar a execução no terminal.
"""

# =========================
# Imports
# =========================
import sqlite3                 # conexão com SQLite
from pathlib import Path       # manipulação de caminhos
import logging                 # logs
import pandas as pd            # análise de dados
import matplotlib.pyplot as plt
import seaborn as sns          # visuais bonitos (paleta/tema)

# =========================
# Caminhos do projeto
# =========================
# ROOT é a raiz do repositório (../ do diretório src)
ROOT = Path(__file__).resolve().parents[1]
# Caminho do banco de dados (criado pelo ETL)
DB_PATH = ROOT / "data" / "processed" / "producao.db"
# Diretórios de saída de relatórios/figuras
REPORTS = ROOT / "reports"
GFX = REPORTS / "graficos"
REPORTS.mkdir(parents=True, exist_ok=True)
GFX.mkdir(parents=True, exist_ok=True)

# =========================
# Logging básico
# =========================
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("analise")

# Tema visual global (Seaborn) — cores suaves e legíveis
sns.set_theme(style="whitegrid", palette="Set2")


def load_db(db_path: Path) -> pd.DataFrame:
    """
    Carrega a tabela 'producao_maquinas' do SQLite e devolve um DataFrame.
    - Retorna DataFrame vazio em caso de erro (sem estourar exceção).
    """
    log.info(f"Carregando SQLite: {db_path}")
    print(f"[analise] abrindo banco: {db_path}")  # também mostra no terminal
    try:
        con = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT * FROM producao_maquinas", con)
        con.close()
        log.info(f"Linhas carregadas: {len(df)}")
        print(f"[analise] linhas carregadas: {len(df)}")
        return df
    except Exception as e:
        log.error(f"Erro ao ler o banco: {e}")
        print(f"[analise] erro ao ler o banco: {e}")
        return pd.DataFrame()


def tratamento(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa/transforma o DataFrame:
    - Converte datas
    - Preenche faltantes
    - Cria métricas auxiliares (falhas_por_hora, semana, mes)
    """
    if df.empty:
        print("[analise] DataFrame vazio — pulando tratamento.")
        return df

    print("[analise] iniciando tratamento…")
    df = df.copy()

    # Datas e horários
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    if "horario_falha" in df.columns:
        df["horario_falha"] = pd.to_datetime(df["horario_falha"], errors="coerce")

    # Remove registros sem data válida
    antes = len(df)
    df.dropna(subset=["data"], inplace=True)
    print(f"[analise] linhas removidas (data inválida): {antes - len(df)}")

    # Corrige/Preenche colunas numéricas
    df["horas_trabalhadas"] = (
        df["horas_trabalhadas"]
        .fillna(10)                 # padrão do cenário
        .clip(lower=0, upper=24)    # segurança
    )
    df["falhas"] = df["falhas"].fillna(0).astype(int).clip(lower=0)
    df["producao"] = df["producao"].fillna(df["producao"].mean()).clip(lower=0)

    # Métrica auxiliar
    df["falhas_por_hora"] = df["falhas"] / df["horas_trabalhadas"].replace(0, 1)

    # Chaves de agregação de tempo
    df["semana"] = df["data"].dt.to_period("W").apply(lambda r: r.start_time)
    df["mes"] = df["data"].dt.to_period("M").astype(str)

    print("[analise] tratamento concluído.")
    return df


def get_processed_data() -> pd.DataFrame:
    """
    Função única para o app:
    - Lê o banco
    - Trata os dados
    """
    df = load_db(DB_PATH)
    if not df.empty:
        df = tratamento(df)
    return df


def monthly_forecast(df: pd.DataFrame) -> pd.DataFrame:
    """
    Previsão mensal simples por máquina:
    - média móvel dos últimos 3 meses como previsão do próximo mês
    - retorna DataFrame com colunas: maquina, mes (previsto), producao_prevista
    """
    if df.empty:
        return pd.DataFrame(columns=["maquina", "mes", "producao_prevista"])

    print("[analise] gerando previsão mensal (média móvel 3 meses)…")
    base = (
        df.groupby(["mes", "maquina"], as_index=False)["producao"]
        .mean()
        .sort_values(["maquina", "mes"])
    )

    # Constrói uma série temporal mensal por máquina e projeta 1 mês
    previsoes = []
    for maq, part in base.groupby("maquina"):
        # garante ordem temporal
        part = part.sort_values("mes").reset_index(drop=True)
        # média móvel 3 meses
        part["mm3"] = part["producao"].rolling(window=3, min_periods=1).mean()
        # previsão = último mm3
        if len(part) == 0:
            continue
        prev_val = float(part["mm3"].iloc[-1])

        # próximo mês (string AAAA-MM)
        ultimo_mes = pd.Period(part["mes"].iloc[-1], freq="M")
        prox_mes = (ultimo_mes + 1).strftime("%Y-%m")
        previsoes.append({"maquina": maq, "mes": prox_mes, "producao_prevista": prev_val})

    prev_df = pd.DataFrame(previsoes)
    print(f"[analise] previsões geradas: {len(prev_df)} linhas")
    return prev_df


def create_plots(df: pd.DataFrame):
    """
    Cria e devolve um dicionário de figuras Matplotlib para uso no Streamlit.
    Inclui:
      - Bar: total de falhas por máquina
      - Linha: produção média diária por máquina
      - Bar: produção média mensal por máquina
    """
    if df.empty:
        return {}, "Não foi possível carregar dados para gráficos."

    plots = {}

    # ---------- 1) Falhas por máquina ----------
    falhas = df.groupby("maquina")["falhas"].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=falhas.index, y=falhas.values, ax=ax1)
    ax1.set_title("Total de Falhas por Máquina", fontsize=14, weight="bold")
    ax1.set_xlabel("Máquina")
    ax1.set_ylabel("Falhas")
    ax1.bar_label(ax1.containers[0], padding=3)
    plots["falhas_por_maquina"] = fig1

    # ---------- 2) Produção média diária ----------
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    sns.lineplot(data=df, x="data", y="producao", hue="maquina", estimator="mean", ax=ax2)
    ax2.set_title("Produção Média por Dia (por máquina)", fontsize=14, weight="bold")
    ax2.set_xlabel("Data")
    ax2.set_ylabel("Produção (peças)")
    ax2.legend(title="Máquina", ncols=3, frameon=True)
    plots["producao_por_dia"] = fig2

    # ---------- 3) Produção média mensal ----------
    base_mensal = df.groupby(["mes", "maquina"], as_index=False)["producao"].mean()
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    for maq, part in base_mensal.groupby("maquina"):
        ax3.plot(part["mes"], part["producao"], marker="o", label=maq)
    ax3.set_title("Produção Média Mensal por Máquina", fontsize=14, weight="bold")
    ax3.set_xlabel("Mês")
    ax3.set_ylabel("Produção (peças)")
    ax3.legend(title="Máquina", ncols=3)
    plt.setp(ax3.get_xticklabels(), rotation=45, ha="right")
    plots["producao_mensal"] = fig3

    return plots, None


# Execução direta (debug)
if __name__ == "__main__":
    print("Executando analise.py diretamente…")
    df_ = get_processed_data()
    if df_.empty:
        print("Não foi possível carregar os dados. Verifique o ETL/arquivo do banco.")
    else:
        print("Dados carregados e tratados com sucesso.")
        _plots, _err = create_plots(df_)
        if _err:
            print(f"Erro ao criar gráficos: {_err}")
        else:
            print("Gráficos criados (use Streamlit para visualizar).")
