
from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo


def download_dataset():
    """
    Baixa o dataset Default of Credit Card Clients
    diretamente do UCI Machine Learning Repository.
    """

    # Identifica a raiz do projeto
    project_root = Path(__file__).resolve().parents[2]

    # Cria diretório de armazenamento
    raw_dir = project_root / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    print("Iniciando download do dataset UCI...")

    # Obtém o dataset oficial (ID 350)
    dataset = fetch_ucirepo(id=350)

    # Separa features e target
    X = dataset.data.features.copy()
    y = dataset.data.targets.copy()

    print("\nDownload concluído!")
    print(f"Features: {X.shape}")
    print(f"Target: {y.shape}")

    # Combina features e target
    df = pd.concat([X, y], axis=1)

    # Salva os dados originais
    output_path = raw_dir / "default_credit_clients_raw.csv"

    df.to_csv(output_path, index=False)

    print(f"\nArquivo salvo em: {output_path}")
    print(f"Dimensão final: {df.shape}")

    print("\nColunas disponíveis:")
    print(df.columns.tolist())

    return df


if __name__ == "__main__":
    download_dataset()
