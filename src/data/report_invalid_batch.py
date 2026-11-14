import pandas as pd
from pandera.errors import SchemaErrors

from src.config import (
    INVALID_DATA_DIR,
    MONITORING_REPORTS_DIR,
    create_project_directories,
)
from src.data.validation import validate_credit_data


def generate_invalid_batch_report():
    create_project_directories()

    input_path = INVALID_DATA_DIR / "invalid_batch.csv"
    output_path = (
        MONITORING_REPORTS_DIR / "invalid_batch_validation_report.csv"
    )

    invalid_batch = pd.read_csv(input_path)

    try:
        validate_credit_data(invalid_batch, lazy=True)
        print("O lote passou pela validação.")
        return

    except SchemaErrors as error:
        failures = error.failure_cases.copy()

        # Mantém apenas as informações mais relevantes
        report = failures[
            ["column", "check", "failure_case", "index"]
        ].copy()

        report.to_csv(output_path, index=False)

        print("LOTE BLOQUEADO: foram encontradas violações.")
        print(f"Total de violações: {len(report)}")
        print("\nViolações por coluna:")
        print(report.groupby("column").size())
        print(f"\nRelatório salvo em: {output_path}")


if __name__ == "__main__":
    generate_invalid_batch_report()