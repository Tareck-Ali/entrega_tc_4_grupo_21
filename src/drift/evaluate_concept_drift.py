
import json
import joblib
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    balanced_accuracy_score,
    confusion_matrix,
)

from src.config import (
    BASELINE_MODEL_PATH,
    PRODUCTION_DATA_DIR,
    MONITORING_REPORTS_DIR,
    create_project_directories,
)


TARGET_COLUMN = "DEFAULT_NEXT_MONTH"

ORIGINAL_PATH = PRODUCTION_DATA_DIR / "production.csv"
CONCEPT_DRIFT_PATH = (
    PRODUCTION_DATA_DIR / "production_concept_drift.csv"
)

OUTPUT_PATH = (
    MONITORING_REPORTS_DIR / "concept_drift_metrics.json"
)


def calculate_metrics(y_true, predictions, probabilities):
    return {
        "precision": float(
            precision_score(y_true, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(y_true, predictions, zero_division=0)
        ),
        "f1_score": float(
            f1_score(y_true, predictions, zero_division=0)
        ),
        "roc_auc": float(
            roc_auc_score(y_true, probabilities)
        ),
        "balanced_accuracy": float(
            balanced_accuracy_score(y_true, predictions)
        ),
        "confusion_matrix": confusion_matrix(
            y_true, predictions
        ).tolist(),
    }


def evaluate_concept_drift():
    create_project_directories()

    model = joblib.load(BASELINE_MODEL_PATH)

    original = pd.read_csv(ORIGINAL_PATH)
    simulated = pd.read_csv(CONCEPT_DRIFT_PATH)

    features = [
        column for column in original.columns
        if column != TARGET_COLUMN
    ]

    # Confirma que as características são idênticas.
    assert original[features].equals(simulated[features])

    X = original[features]

    y_original = original[TARGET_COLUMN]
    y_simulated = simulated[TARGET_COLUMN]

    # As previsões são calculadas uma única vez.
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    original_metrics = calculate_metrics(
        y_original,
        predictions,
        probabilities,
    )

    simulated_metrics = calculate_metrics(
        y_simulated,
        predictions,
        probabilities,
    )

    results = {
        "model": "baseline_logistic_regression",
        "records": len(original),
        "changed_labels": int(
            (y_original != y_simulated).sum()
        ),
        "original": original_metrics,
        "simulated": simulated_metrics,
        "variation": {
            metric: simulated_metrics[metric]
            - original_metrics[metric]
            for metric in [
                "precision",
                "recall",
                "f1_score",
                "roc_auc",
                "balanced_accuracy",
            ]
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            indent=4,
            ensure_ascii=False,
        )

    print("\nAVALIAÇÃO DE CONCEPT DRIFT CONCLUÍDA")

    print("\nMÉTRICAS ORIGINAIS")
    for metric, value in original_metrics.items():
        print(f"{metric}: {value}")

    print("\nMÉTRICAS SIMULADAS")
    for metric, value in simulated_metrics.items():
        print(f"{metric}: {value}")

    print("\nVARIAÇÃO (SIMULADO - ORIGINAL)")
    for metric, value in results["variation"].items():
        print(f"{metric}: {value:+.4f}")

    print(f"\nResultados salvos em: {OUTPUT_PATH}")


if __name__ == "__main__":
    evaluate_concept_drift()
