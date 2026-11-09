
import pandas as pd

from ucimlrepo import fetch_ucirepo
from src.config import RAW_DATASET_PATH, create_project_directories


def download_dataset():
    create_project_directories()

    print("Iniciando download do dataset UCI...")

    dataset = fetch_ucirepo(id=350)

    X = dataset.data.features.copy()
    y = dataset.data.targets.copy()

    df = pd.concat([X, y], axis=1)

    df.to_csv(RAW_DATASET_PATH, index=False)

    print(f"Arquivo salvo em: {RAW_DATASET_PATH}")
    print(f"Dimensão final: {df.shape}")

    return df


if __name__ == "__main__":
    download_dataset()
