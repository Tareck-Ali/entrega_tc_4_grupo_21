import pandas as pd

from src.config import (
    RAW_DATASET_PATH,
    INVALID_DATA_DIR,
    create_project_directories,
)
from src.data.preprocessing import normalize_column_names


def create_invalid_batch():
    create_project_directories()

    # Carrega o dataset original
    raw_data = pd.read_csv(RAW_DATASET_PATH)

    # Normaliza os nomes das colunas
    data = normalize_column_names(raw_data)

    # Cria um lote de 1.000 registros
    invalid_batch = data.sample(
        n=1000,
        random_state=42
    ).copy()

    # Introduz violações intencionais
    invalid_batch.iloc[0, invalid_batch.columns.get_loc("PAY_AMT1")] = -100
    invalid_batch.iloc[1, invalid_batch.columns.get_loc("SEX")] = 3
    invalid_batch.iloc[2, invalid_batch.columns.get_loc("DEFAULT_NEXT_MONTH")] = 2

    # Salva o lote inválido
    output_path = INVALID_DATA_DIR / "invalid_batch.csv"
    invalid_batch.to_csv(output_path, index=False)

    print(f"Lote inválido criado: {output_path}")
    print(f"Registros: {len(invalid_batch)}")


if __name__ == "__main__":
    create_invalid_batch()