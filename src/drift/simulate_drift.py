
import numpy as np
import pandas as pd

from src.config import (
    PRODUCTION_DATA_DIR,
    create_project_directories,
)
from src.data.validation import validate_credit_data


RANDOM_STATE = 42
DRIFTED_DATA_PATH = PRODUCTION_DATA_DIR / "production_drift.csv"


def simulate_drift():
    create_project_directories()

    original_data = pd.read_csv(
        PRODUCTION_DATA_DIR / "production.csv"
    )

    drifted_data = original_data.copy()

    rng = np.random.default_rng(RANDOM_STATE)

    # Seleciona 60% dos registros para receber as alterações.
    sample_size = int(len(drifted_data) * 0.60)

    selected_positions = rng.choice(
        len(drifted_data),
        size=sample_size,
        replace=False,
    )

    selected_indices = drifted_data.index[selected_positions]

    # Drift 1: redução de 30% no limite de crédito.
    new_limits = (
        drifted_data.loc[selected_indices, "LIMIT_BAL"] * 0.70
    ).round(-3)

    drifted_data.loc[selected_indices, "LIMIT_BAL"] = (
        new_limits.clip(lower=10000).astype(int)
    )

    # Drift 2: redução de 5 anos na idade dos clientes.
    new_ages = (
        drifted_data.loc[selected_indices, "AGE"] - 5
    )

    drifted_data.loc[selected_indices, "AGE"] = (
        new_ages.clip(lower=18).astype(int)
    )

    # Confirma que o alvo não foi alterado.
    assert drifted_data["DEFAULT_NEXT_MONTH"].equals(
        original_data["DEFAULT_NEXT_MONTH"]
    )

    # Valida o lote simulado pelo contrato de dados.
    validate_credit_data(drifted_data)

    # Salva em um arquivo separado.
    drifted_data.to_csv(DRIFTED_DATA_PATH, index=False)

    print("SIMULAÇÃO DE DATA DRIFT CONCLUÍDA")
    print(f"Registros originais: {len(original_data)}")
    print(f"Registros alterados: {sample_size}")
    print(f"Arquivo salvo em: {DRIFTED_DATA_PATH}")

    print("\nComparação das variáveis:")

    for column in ["LIMIT_BAL", "AGE"]:
        print(f"\n{column}")
        print(
            f"Média original: {original_data[column].mean():.2f}"
        )
        print(
            f"Média simulada: {drifted_data[column].mean():.2f}"
        )


if __name__ == "__main__":
    simulate_drift()
