import json
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    balanced_accuracy_score,
    confusion_matrix,
)

from src.config import (
    REFERENCE_DATA_DIR,
    PRODUCTION_DATA_DIR,
    BASELINE_MODEL_PATH,
    BASELINE_METRICS_PATH,
    create_project_directories,
)


TARGET = "DEFAULT_NEXT_MONTH"

CATEGORICAL_FEATURES = [
    "SEX", "EDUCATION", "MARRIAGE",
    "PAY_0", "PAY_2", "PAY_3",
    "PAY_4", "PAY_5", "PAY_6",
]


def train_baseline():
    create_project_directories()

    # Carregar os conjuntos
    reference = pd.read_csv(
        REFERENCE_DATA_DIR / "reference.csv"
    )

    production = pd.read_csv(
        PRODUCTION_DATA_DIR / "production.csv"
    )

    # Separar variáveis explicativas e alvo
    X_train = reference.drop(columns=[TARGET])
    y_train = reference[TARGET]

    X_test = production.drop(columns=[TARGET])
    y_test = production[TARGET]

    numerical_features = [
        column for column in X_train.columns
        if column not in CATEGORICAL_FEATURES
    ]

    # Pré-processamento
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                CATEGORICAL_FEATURES,
            ),
            (
                "numerical",
                StandardScaler(),
                numerical_features,
            ),
        ]
    )

    # Modelo
    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                LogisticRegression(
                    max_iter=2000,
                    class_weight="balanced",
                    random_state=42,
                ),
            ),
        ]
    )

    # Treinamento exclusivamente com dados de referência
    model.fit(X_train, y_train)

    # Avaliação na produção
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    metrics = {
        "model": "Logistic Regression",
        "reference_records": len(reference),
        "production_records": len(production),
        "precision": float(
            precision_score(y_test, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(y_test, predictions, zero_division=0)
        ),
        "f1_score": float(
            f1_score(y_test, predictions, zero_division=0)
        ),
        "roc_auc": float(
            roc_auc_score(y_test, probabilities)
        ),
        "balanced_accuracy": float(
            balanced_accuracy_score(y_test, predictions)
        ),
        "confusion_matrix": confusion_matrix(
            y_test, predictions
        ).tolist(),
    }

    # Salvar modelo
    joblib.dump(model, BASELINE_MODEL_PATH)

    # Salvar métricas
    with open(BASELINE_METRICS_PATH, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4, ensure_ascii=False)

    print("\nTreinamento concluído!")
    print(f"Modelo salvo em: {BASELINE_MODEL_PATH}")

    print("\nMétricas de avaliação:")
    for metric, value in metrics.items():
        print(f"{metric}: {value}")


if __name__ == "__main__":
    train_baseline()