
import pandas as pd
import pytest

from src.config import RAW_DATASET_PATH
from src.data.preprocessing import normalize_column_names
from src.data.validation import validate_credit_data


@pytest.fixture
def valid_data():
    raw_data = pd.read_csv(RAW_DATASET_PATH)

    return normalize_column_names(raw_data)


def test_valid_dataset_passes(valid_data):
    validated = validate_credit_data(valid_data)

    assert validated.shape == (30000, 24)


def test_negative_payment_fails(valid_data):
    invalid_data = valid_data.copy()
    invalid_data.loc[0, "PAY_AMT1"] = -100

    with pytest.raises(Exception):
        validate_credit_data(invalid_data)


def test_invalid_target_fails(valid_data):
    invalid_data = valid_data.copy()
    invalid_data.loc[0, "DEFAULT_NEXT_MONTH"] = 2

    with pytest.raises(Exception):
        validate_credit_data(invalid_data)


def test_invalid_sex_fails(valid_data):
    invalid_data = valid_data.copy()
    invalid_data.loc[0, "SEX"] = 3

    with pytest.raises(Exception):
        validate_credit_data(invalid_data)
