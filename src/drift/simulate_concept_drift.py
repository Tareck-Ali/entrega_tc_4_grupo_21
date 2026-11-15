
import numpy as np
import pandas as pd

from src.config import (
    PRODUCTION_DATA_DIR,
    create_project_directories,
)
from src.data.validation import validate_credit_data


RANDOM_STATE = 42

ORIGINAL_PATH = PRODUCTION_DATA_DIR / "production.csv"
CONCEPT_DRIFT_PATH = (
    PRODUCTION_DATA_DIR / "production_concept_drift.csv"
)

TARGET_COLUMN = "DEFAULT_NEXT_MONTH"


def simulate_concept_drift():
    create_project_directories()

    original_data = pd.read_csv(ORIGINAL_PATH)
    drifted_data = original_data.copy()

    rng = np.random.default_rng(RANDOM_STATE)

    # Seleciona clientes com atraso de pagamento registrado.
    eligible_indices = drifted_data.index[
        drifted_data["PAY_0"] >= 1
    ]

    # Inverte o rótulo de 50% desse grupo.
    sample_size = int(len(eligible_indices) * 0.50)

    selected_indices = rng.choice(
        eligible_indices.to_numpy(),
        size=sample_size,
        replace=False,
    )

    drifted_data.loc[selected_indices, TARGET_COLUMN] = (
        1 - drifted_data.loc[selected_indices, TARGET_COLUMN]
    )

    # Confirma que somente o alvo foi alterado.
    feature_columns = [
        column for column in original_data.columns
        if column != TARGET_COLUMN
    ]

    assert drifted_data[feature_columns].equals(
        original_data[feature_columns]
    )

    changed_labels = (
        drifted_data[TARGET_COLUMN]
        != original_data[TARGET_COLUMN]
    ).sum()

    assert changed_labels == sample_size

    # Valida o lote com o contrato de dados.
    validate_credit_data(drifted_data)

    drifted_data.to_csv(
        CONCEPT_DRIFT_PATH,
        index=False,
    )

    print("SIMULAÇÃO DE CONCEPT DRIFT CONCLUÍDA")
    print(f"Registros originais: {len(original_data)}")
    print(f"Clientes elegíveis: {len(eligible_indices)}")
    print(f"Rótulos alterados: {changed_labels}")

    print("\nTaxa de inadimplência:")
    print(
        "Original: "
        f"{original_data[TARGET_COLUMN].mean():.2%}"
    )
    print(
        "Simulada: "
        f"{drifted_data[TARGET_COLUMN].mean():.2%}"
    )

    print(f"\nArquivo salvo em: {CONCEPT_DRIFT_PATH}")


if __name__ == "__main__":
    simulate_concept_drift()
