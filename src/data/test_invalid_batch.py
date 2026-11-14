import pandas as pd
import pytest

from pandera.errors import SchemaError, SchemaErrors

from src.config import INVALID_DATA_DIR
from src.data.validation import validate_credit_data


def test_invalid_batch_is_blocked():
    file_path = INVALID_DATA_DIR / "invalid_batch.csv"

    invalid_batch = pd.read_csv(file_path)

    with pytest.raises((SchemaError, SchemaErrors)):
        validate_credit_data(invalid_batch)