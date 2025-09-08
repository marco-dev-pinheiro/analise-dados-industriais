

from pathlib import Path
import numpy as np
import pandas as pd

# ========= Caminhos =========
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH = RAW_DIR / "producao_raw.csv"

# ========= Parâmetros globais =========
np.random.seed(42)

# Conjunto de máquinas (ex.: 8 máquinas)
MAQUINAS = [f"A{n}" for n in range(1, 6)] + [f"B{n}" for n in range(1, 4)]

# Máquinas com falhas regulares (probabilidade base maior)
FALHA_REGULAR = {"A3", "B2"}

# Período de 180 dias até hoje
datas = pd.date_range(end=pd.Timestamp.today().normalize(), periods=180, freq="D")

# ========= Simulação =========
rows = []
for dia in datas:
    # janelas de trabalho (08:00–18:00) = 10 horas
    horas_trab = 10.0
    inicio = pd.Timestamp(dia.date()) + pd.Timedelta(hours=8)   # 08:00
    fim = inicio + pd.Timedelta(hours=10)                       # 18:00

    for maq in MAQUINAS:
        # taxa base de produção por hora por máquina, com pequena variação
        taxa_base = np.random.normal(loc=7.5, scale=1.2)  # peças/hora
        # ruído diário
        ruido = np.random.normal(loc=0.0, scale=0.8)
        producao = max(0.0, horas_trab * max(0.0, taxa_base + ruido))

        # probabilidade de falha
        p_base = 0.03
        if maq in FALHA_REGULAR:
            p_base = 0.10  # máquinas com falhas regulares

        falhou = np.random.binomial(1, p_base)

        # horário da falha (se ocorrer)
        if falhou == 1:
            # escolhe um momento aleatório entre 08:00 e 18:00
            delta = np.random.uniform(0, (fim - inicio).total_seconds())
            horario_falha = inicio + pd.Timedelta(seconds=delta)
        else:
            horario_falha = pd.NaT

        rows.append(
            (
                maq,
                dia.strftime("%Y-%m-%d"),
                horas_trab,
                falhou,
                round(producao, 2),
                None if pd.isna(horario_falha) else horario_falha.isoformat(timespec="minutes"),
            )
        )

# ========= DataFrame final =========
df = pd.DataFrame(
    rows,
    columns=[
        "maquina",
        "data",
        "horas_trabalhadas",
        "falhas",
        "producao",
        "horario_falha",
    ],
)

# Pequenos NaNs aleatórios para simular realidade (sem sobrecarga)
for col in ["producao"]:
    mask = np.random.rand(len(df)) < 0.01
    df.loc[mask, col] = np.nan

# ========= Salvar =========
df.to_csv(CSV_PATH, index=False)
print(f"[generate_data] dataset gerado: {CSV_PATH} | linhas: {len(df)}")
print(f"[generate_data] máquinas com falhas regulares: {sorted(FALHA_REGULAR)}")