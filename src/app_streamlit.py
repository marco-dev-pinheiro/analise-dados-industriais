"""
Dashboard Streamlit — lê do SQLite (via analise.py) e exibe análises/gráficos.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import analise  # nossas funções utilitárias

st.set_page_config(page_title="Análise de Produção Industrial", layout="wide", page_icon="📊")

# =============================
# 1) Carregar dados do SQLite
# =============================
@st.cache_data(show_spinner=True)
def carregar_dados_tratados() -> pd.DataFrame:
    # usa o pipeline de analise.py
    df = analise.get_processed_data()
    return df

df = carregar_dados_tratados()

# Guarda um alerta se o df estiver vazio
if df.empty:
    st.error("Não foi possível carregar dados do banco. Rode o ETL (producao.py) primeiro.")
    st.stop()

# =============================
# 2) Título e descrição
# =============================
st.title("📊 Análise de Produção Industrial")
st.markdown(
    """
    Visualize **produção diária, semanal e mensal**, **falhas por máquina** e uma
    **previsão simples** para o próximo mês (média móvel 3 meses).
    """
)

# =============================
# 3) Filtros
# =============================
col_f1, col_f2 = st.columns([2, 1])
with col_f1:
    maquinas = st.multiselect(
        "Selecione as máquinas:",
        options=sorted(df["maquina"].unique()),
        default=sorted(df["maquina"].unique()),
    )
with col_f2:
    intervalo = st.date_input(
        "Período:",
        value=(df["data"].min().date(), df["data"].max().date()),
        min_value=df["data"].min().date(),
        max_value=df["data"].max().date(),
    )

# Aplica filtros com cópia segura
df_filtrado = df[(df["maquina"].isin(maquinas)) &
                 (df["data"].between(pd.to_datetime(intervalo[0]), pd.to_datetime(intervalo[1])))]
df_filtrado = df_filtrado.copy()

# =============================
# 4) Métricas rápidas (cards)
# =============================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Máquinas selecionadas", len(maquinas))
with col2:
    st.metric("Dias no período", df_filtrado["data"].nunique())
with col3:
    st.metric("Peças (média diária)", f"{df_filtrado['producao'].mean():,.0f}")
with col4:
    st.metric("Falhas (total)", int(df_filtrado["falhas"].sum()))

st.divider()

# =============================
# 5) Gráficos principais
# =============================
plots, err = analise.create_plots(df_filtrado)
if err:
    st.error(err)
else:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🔧 Falhas por Máquina")
        st.pyplot(plots["falhas_por_maquina"])
    with c2:
        st.subheader("📅 Produção Média Diária")
        st.pyplot(plots["producao_por_dia"])

    st.subheader("📊 Produção Mensal")
    st.pyplot(plots["producao_mensal"])

# =============================
# 6) Agregações (diária, semanal, mensal)
# =============================
st.divider()
st.subheader("📋 Tabelas de Resumo")

# Diária
base_diaria = (
    df_filtrado.groupby(["data", "maquina"], as_index=False)["producao"].mean()
    .sort_values(["data", "maquina"])
)
# Semanal
df_filtrado["semana"] = df_filtrado["data"].dt.to_period("W").apply(lambda r: r.start_time)
base_semanal = (
    df_filtrado.groupby(["semana", "maquina"], as_index=False)["producao"].mean()
    .sort_values(["semana", "maquina"])
)
# Mensal
df_filtrado["mes"] = df_filtrado["data"].dt.to_period("M").astype(str)
base_mensal = (
    df_filtrado.groupby(["mes", "maquina"], as_index=False)["producao"].mean()
    .sort_values(["mes", "maquina"])
)

tab1, tab2, tab3 = st.tabs(["Diária", "Semanal", "Mensal"])
with tab1:
    st.dataframe(base_diaria)
with tab2:
    st.dataframe(base_semanal)
with tab3:
    st.dataframe(base_mensal.pivot(index="mes", columns="maquina", values="producao"))

# =============================
# 7) Previsão mensal simples
# =============================
st.divider()
st.subheader("🔮 Previsão mensal (média móvel 3 meses)")
prev = analise.monthly_forecast(df_filtrado)
if prev.empty:
    st.info("Sem dados suficientes para previsão.")
else:
    st.dataframe(prev)
