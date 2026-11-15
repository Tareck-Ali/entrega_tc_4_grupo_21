
import json

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import (
    PREDICTION_LOG_PATH,
    PREDICTION_BATCH_SUMMARY_PATH,
    BASELINE_METRICS_PATH,
)


# --------------------------------------------------
# Configuração da página
# --------------------------------------------------

st.set_page_config(
    page_title="Credit Default - Observabilidade",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Dashboard de Observabilidade")
st.caption(
    "Monitoramento do modelo baseline de previsão de inadimplência"
)


# --------------------------------------------------
# Carregamento dos dados
# --------------------------------------------------

@st.cache_data
def load_data():
    logs = pd.read_csv(PREDICTION_LOG_PATH)

    summaries = pd.read_json(
        PREDICTION_BATCH_SUMMARY_PATH,
        lines=True,
    )

    with open(
        BASELINE_METRICS_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        baseline_metrics = json.load(file)

    return logs, summaries, baseline_metrics


if st.button("🔄 Atualizar dados"):
    st.cache_data.clear()

try:
    logs, summaries, baseline_metrics = load_data()

except FileNotFoundError as error:
    st.error(f"Arquivo não encontrado: {error}")
    st.stop()

if logs.empty or summaries.empty:
    st.warning("Ainda não existem registros de monitoramento.")
    st.stop()


# --------------------------------------------------
# Indicadores principais
# --------------------------------------------------

latest_batch = summaries.iloc[-1]

st.subheader("1. Saúde do pipeline")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Registros processados",
    f"{int(latest_batch['batch_size']):,}".replace(",", "."),
)

col2.metric(
    "Latência do lote",
    f"{latest_batch['batch_latency_ms']:.2f} ms",
)

col3.metric(
    "Previsões nulas",
    int(latest_batch["null_predictions"]),
)

col4.metric(
    "Probabilidades nulas",
    int(latest_batch["null_probabilities"]),
)


# --------------------------------------------------
# Distribuição das previsões
# --------------------------------------------------

st.divider()
st.subheader("2. Distribuição das previsões")

class_distribution = (
    logs["predicted_class"]
    .value_counts()
    .sort_index()
    .rename_axis("Classe")
    .reset_index(name="Quantidade")
)

class_distribution["Classe"] = (
    class_distribution["Classe"].map({
        0: "Não inadimplente",
        1: "Inadimplente",
    })
)

fig_distribution = px.pie(
    class_distribution,
    names="Classe",
    values="Quantidade",
    title="Distribuição das classes previstas",
    hole=0.4,
)

st.plotly_chart(
    fig_distribution,
    use_container_width=True,
)


# --------------------------------------------------
# Comparação entre previsto e real
# --------------------------------------------------

st.divider()
st.subheader("3. Previsões versus resultados reais")

if logs["actual_class"].notna().any():

    comparison = pd.DataFrame({
        "Real": logs["actual_class"].value_counts(normalize=True),
        "Previsto": logs["predicted_class"].value_counts(normalize=True),
    }).fillna(0)

    comparison.index = comparison.index.map({
        0: "Não inadimplente",
        1: "Inadimplente",
    })

    comparison = (
        comparison.rename_axis("Classe")
        .reset_index()
        .melt(
            id_vars="Classe",
            var_name="Tipo",
            value_name="Proporção",
        )
    )

    fig_comparison = px.bar(
        comparison,
        x="Classe",
        y="Proporção",
        color="Tipo",
        barmode="group",
        title="Distribuição real e prevista",
        text_auto=".1%",
    )

    st.plotly_chart(
        fig_comparison,
        use_container_width=True,
    )

else:
    st.info("Resultados reais ainda não estão disponíveis.")


# --------------------------------------------------
# Histórico dos lotes
# --------------------------------------------------

st.divider()
st.subheader("4. Histórico de processamento")

history = summaries.copy()

history["batch_number"] = range(1, len(history) + 1)

fig_latency = px.line(
    history,
    x="batch_number",
    y="batch_latency_ms",
    markers=True,
    title="Latência por lote",
    labels={
        "batch_number": "Número do lote",
        "batch_latency_ms": "Latência (ms)",
    },
)

st.plotly_chart(
    fig_latency,
    use_container_width=True,
)


# --------------------------------------------------
# Métricas do modelo baseline
# --------------------------------------------------

st.divider()
st.subheader("5. Métricas do modelo baseline")

metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

metric_col1.metric(
    "Precision",
    f"{baseline_metrics['precision']:.2%}",
)

metric_col2.metric(
    "Recall",
    f"{baseline_metrics['recall']:.2%}",
)

metric_col3.metric(
    "F1-score",
    f"{baseline_metrics['f1_score']:.2%}",
)

metric_col4.metric(
    "ROC-AUC",
    f"{baseline_metrics['roc_auc']:.2%}",
)


# --------------------------------------------------
# Informações complementares
# --------------------------------------------------

st.divider()

st.subheader("6. Detalhes dos lotes")

st.dataframe(
    summaries,
    use_container_width=True,
)

st.caption(
    "Projeto Tech Challenge — Monitoramento de modelo de crédito"
)
