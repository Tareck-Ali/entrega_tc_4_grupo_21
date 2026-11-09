
from src.config import COLUMN_RENAME_MAP


def normalize_column_names(df):
    """
    Padroniza os nomes das colunas do dataset UCI.
    Não altera os dados originais.
    """

    expected_columns = set(COLUMN_RENAME_MAP.keys())
    received_columns = set(df.columns)

    missing_columns = expected_columns - received_columns
    unexpected_columns = received_columns - expected_columns

    if missing_columns or unexpected_columns:
        raise ValueError(
            f"Colunas ausentes: {sorted(missing_columns)}. "
            f"Colunas inesperadas: {sorted(unexpected_columns)}."
        )

    return df.rename(columns=COLUMN_RENAME_MAP)
