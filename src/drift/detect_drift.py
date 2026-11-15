
import pandas as pd

from evidently import Report
from evidently.presets import DataDriftPreset

from src.config import (
    REFERENCE_DATA_DIR,
    PRODUCTION_DATA_DIR,
    DRIFT_REPORTS_DIR,
    create_project_directories,
)


TARGET_COLUMN = "DEFAULT_NEXT_MONTH"

REFERENCE_PATH = REFERENCE_DATA_DIR / "reference.csv"
PRODUCTION_PATH = PRODUCTION_DATA_DIR / "production_drift.csv"
REPORT_PATH = DRIFT_REPORTS_DIR / "data_drift_report.html"
DRIFT_JSON_PATH = DRIFT_REPORTS_DIR / "data_drift_summary.json"

def detect_drift():
    create_project_directories()

    reference = pd.read_csv(REFERENCE_PATH)
    production = pd.read_csv(PRODUCTION_PATH)

    # Exclui o alvo: queremos avaliar somente as features.
    reference_features = reference.drop(columns=[TARGET_COLUMN])
    production_features = production.drop(columns=[TARGET_COLUMN])

    # Gera o relatório de Data Drift.
    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    evaluation = report.run(
        reference_data=reference_features,
        current_data=production_features,
    )

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    evaluation.save_html(str(REPORT_PATH))
    evaluation.save_json(str(DRIFT_JSON_PATH))

    print("ANÁLISE DE DATA DRIFT CONCLUÍDA")
    print(f"Registros de referência: {len(reference_features)}")
    print(f"Registros de produção: {len(production_features)}")
    print(f"Relatório salvo em: {REPORT_PATH}")


if __name__ == "__main__":
    detect_drift()
