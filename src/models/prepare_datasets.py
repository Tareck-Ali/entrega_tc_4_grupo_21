import pandas as pd
from sklearn.model_selection import train_test_split

from src.config import (
    RAW_DATASET_PATH,
    REFERENCE_DATA_DIR,
    PRODUCTION_DATA_DIR,
    create_project_directories,
)
from src.data.preprocessing import normalize_column_names
from src.data.validation import validate_credit_data


TARGET = "DEFAULT_NEXT_MONTH"


def prepare_datasets():
    create_project_directories()

    # Carregar dataset original
    raw_data = pd.read_csv(RAW_DATASET_PATH)

    # Normalizar nomes das colunas
    data = normalize_column_names(raw_data)

    # Validar os dados
    data = validate_credit_data(data)

    # Separar referência e produção
    reference_data, production_data = train_test_split(
        data,
        test_size=0.30,
        random_state=42,
        stratify=data[TARGET],
    )

    # Salvar os conjuntos
    reference_path = REFERENCE_DATA_DIR / "reference.csv"
    production_path = PRODUCTION_DATA_DIR / "production.csv"

    reference_data.to_csv(reference_path, index=False)
    production_data.to_csv(production_path, index=False)

    print("Separação concluída!")
    print(f"Referência: {len(reference_data)} registros")
    print(f"Produção: {len(production_data)} registros")

    print("\nDistribuição do alvo na referência:")
    print(reference_data[TARGET].value_counts(normalize=True))

    print("\nDistribuição do alvo na produção:")
    print(production_data[TARGET].value_counts(normalize=True))


if __name__ == "__main__":
    prepare_datasets()