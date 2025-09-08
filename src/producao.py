"""
ETL: lê data/raw/producao_raw.csv, valida/limpa e grava em SQLite (data/processed/producao.db).
Inclui logs claros e tratamento robusto.
"""

from pathlib import Path
import logging
import sqlite3
import pandas as pd

# ============ Caminhos ============
ROOT = Path(__file__).resolve().parents[1]
RAW_CSV = ROOT / "data" / "raw" / "producao_raw.csv"
PROC_DIR = ROOT / "data" / "processed"
PROC_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = PROC_DIR / "producao.db"

# ============ Logging ============
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("etl")

# Colunas essenciais (horario_falha é opcional)
REQUIRED = {"maquina", "data", "horas_trabalhadas", "falhas", "producao"}


def load_csv(path: Path) -> pd.DataFrame:
    """Lê o CSV e checa colunas obrigatórias."""
    log.info(f"Lendo CSV: {path}")
    df = pd.read_csv(path)
    df.columns = df.columns.str.lower()
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Colunas faltando no CSV: {missing}")
    log.info(f"Linhas lidas: {len(df)}")
    return df


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpeza/normalização:
    - converte datas
    - garante tipos numéricos e faixas válidas
    - preenche faltantes com valores seguros/médias
    """
    log.info("Limpando/validando dados…")
    df = df.copy()

    # Datas
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    if "horario_falha" in df.columns:
        df["horario_falha"] = pd.to_datetime(df["horario_falha"], errors="coerce")

    antes = len(df)
    df.dropna(subset=["data"], inplace=True)
    log.info(f"Removidos {antes - len(df)} registros com data inválida")

    # Tipos numéricos + bounds
    df["horas_trabalhadas"] = (
        pd.to_numeric(df["horas_trabalhadas"], errors="coerce")
        .fillna(10)
        .clip(lower=0, upper=24)
    )
    df["falhas"] = pd.to_numeric(df["falhas"], errors="coerce").fillna(0).astype(int).clip(lower=0)
    df["producao"] = pd.to_numeric(df["producao"], errors="coerce").fillna(df["producao"].mean()).clip(lower=0)

    # Chaves coerentes
    df["maquina"] = df["maquina"].astype(str)

    log.info("Limpeza concluída.")
    return df


def save_to_sqlite(df: pd.DataFrame, db_path: Path) -> None:
    """Persiste no SQLite (substitui a tabela)."""
    log.info(f"Gravando no SQLite: {db_path}")
    con = sqlite3.connect(db_path)
    df.to_sql("producao_maquinas", con, if_exists="replace", index=False)
    con.close()
    log.info("ETL finalizado com sucesso.")


if __name__ == "__main__":
    try:
        df_in = load_csv(RAW_CSV)
        df_ok = clean_df(df_in)
        save_to_sqlite(df_ok, DB_PATH)
    except Exception as e:
        log.exception(f"Erro no ETL: {e}")
