
from pathlib import Path

# Raiz do projeto
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Diretórios principais
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
REFERENCE_DATA_DIR = DATA_DIR / "reference"
PRODUCTION_DATA_DIR = DATA_DIR / "production"
INVALID_DATA_DIR = DATA_DIR / "invalid"

REPORTS_DIR = PROJECT_ROOT / "reports"
DRIFT_REPORTS_DIR = REPORTS_DIR / "drift"
MONITORING_REPORTS_DIR = REPORTS_DIR / "monitoring"

# Arquivos de dados
DATASET_FILENAME = "default_credit_clients_raw.csv"
RAW_DATASET_PATH = RAW_DATA_DIR / DATASET_FILENAME


def create_project_directories():
    """Cria os diretórios necessários, caso ainda não existam."""
    directories = [
        RAW_DATA_DIR,
        REFERENCE_DATA_DIR,
        PRODUCTION_DATA_DIR,
        INVALID_DATA_DIR,
        DRIFT_REPORTS_DIR,
        MONITORING_REPORTS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


COLUMN_RENAME_MAP = {
    "X1": "LIMIT_BAL",
    "X2": "SEX",
    "X3": "EDUCATION",
    "X4": "MARRIAGE",
    "X5": "AGE",
    "X6": "PAY_0",
    "X7": "PAY_2",
    "X8": "PAY_3",
    "X9": "PAY_4",
    "X10": "PAY_5",
    "X11": "PAY_6",
    "X12": "BILL_AMT1",
    "X13": "BILL_AMT2",
    "X14": "BILL_AMT3",
    "X15": "BILL_AMT4",
    "X16": "BILL_AMT5",
    "X17": "BILL_AMT6",
    "X18": "PAY_AMT1",
    "X19": "PAY_AMT2",
    "X20": "PAY_AMT3",
    "X21": "PAY_AMT4",
    "X22": "PAY_AMT5",
    "X23": "PAY_AMT6",
    "Y": "DEFAULT_NEXT_MONTH",
}
