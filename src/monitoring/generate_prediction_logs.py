import json
import time
from datetime import datetime, timezone

import joblib
import pandas as pd

from src.config import (
    BASELINE_MODEL_PATH,
    PRODUCTION_DATA_DIR,
    PREDICTION_LOG_PATH,
    PREDICTION_BATCH_SUMMARY_PATH,
    create_project_directories,
)


TARGET = "DEFAULT_NEXT_MONTH"


def generate_prediction_logs():
    create_project_directories()

    # Carregar modelo e dados de produção
    model = joblib.load(BASELINE_MODEL_PATH)

    production_data = pd.read_csv(
        PRODUCTION_DATA_DIR / "production.csv"
    )

    # Separar features e variável-alvo
    if TARGET in production_data.columns:
        y_true = production_data[TARGET].copy()
        X = production_data.drop(columns=[TARGET])
    else:
        y_true = None
        X = production_data.copy()

    # Identificação do lote
    timestamp = datetime.now(timezone.utc)
    timestamp_str = timestamp.isoformat()
    batch_id = timestamp.strftime("%Y%m%dT%H%M%S%fZ")

    # Medir tempo de inferência
    start_time = time.perf_counter()

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    end_time = time.perf_counter()

    latency_ms = (end_time - start_time) * 1000

    # Criar registros de previsão
    logs = pd.DataFrame({
        "batch_id": batch_id,
        "prediction_id": [
            f"{batch_id}_{i:06d}"
            for i in range(1, len(X) + 1)
        ],
        "prediction_timestamp_utc": timestamp_str,
        "predicted_probability_default": probabilities,
        "predicted_class": predictions,
        "actual_class": (
            y_true.to_numpy()
            if y_true is not None
            else None
        ),
    })

    # Indicadores de saúde
    null_predictions = int(
        logs["predicted_class"].isna().sum()
    )

    null_probabilities = int(
        logs["predicted_probability_default"].isna().sum()
    )

    predicted_default_rate = float(
        (logs["predicted_class"] == 1).mean()
    )

    summary = {
        "batch_id": batch_id,
        "timestamp_utc": timestamp_str,
        "batch_size": int(len(logs)),
        "batch_latency_ms": float(latency_ms),
        "average_latency_per_record_ms": float(
            latency_ms / len(logs)
        ),
        "throughput_records_per_second": float(
            len(logs) / (latency_ms / 1000)
        ) if latency_ms > 0 else None,
        "null_predictions": null_predictions,
        "null_probabilities": null_probabilities,
        "predicted_default_rate": predicted_default_rate,
        "actual_default_rate": (
            float(y_true.mean())
            if y_true is not None
            else None
        ),
    }

    # Acrescentar logs sem apagar execuções anteriores
    logs.to_csv(
        PREDICTION_LOG_PATH,
        mode="a",
        header=not PREDICTION_LOG_PATH.exists(),
        index=False,
    )

    # Guardar um resumo por execução (JSON Lines)
    with open(
        PREDICTION_BATCH_SUMMARY_PATH,
        "a",
        encoding="utf-8",
    ) as file:
        file.write(json.dumps(summary, ensure_ascii=False) + "\n")

    print("\nGeração de logs concluída!")
    print(f"Batch ID: {batch_id}")
    print(f"Registros processados: {len(logs)}")
    print(f"Latência do lote: {latency_ms:.2f} ms")
    print(f"Previsões nulas: {null_predictions}")
    print(f"Probabilidades nulas: {null_probabilities}")
    print(f"Taxa prevista de inadimplência: {predicted_default_rate:.2%}")
    print(f"\nLogs salvos em: {PREDICTION_LOG_PATH}")
    print(f"Resumo salvo em: {PREDICTION_BATCH_SUMMARY_PATH}")


if __name__ == "__main__":
    generate_prediction_logs()