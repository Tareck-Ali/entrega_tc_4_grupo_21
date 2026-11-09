
import pandera.pandas as pa
from pandera import Check, Column


# Colunas numéricas de cada grupo
payment_delay_columns = [
    "PAY_0", "PAY_2", "PAY_3",
    "PAY_4", "PAY_5", "PAY_6"
]

bill_amount_columns = [
    "BILL_AMT1", "BILL_AMT2", "BILL_AMT3",
    "BILL_AMT4", "BILL_AMT5", "BILL_AMT6"
]

payment_amount_columns = [
    "PAY_AMT1", "PAY_AMT2", "PAY_AMT3",
    "PAY_AMT4", "PAY_AMT5", "PAY_AMT6"
]


# Definição do contrato
columns = {
    "LIMIT_BAL": Column(
        int, Check.greater_than(0), nullable=False
    ),
    "SEX": Column(
        int, Check.isin([1, 2]), nullable=False
    ),
    "EDUCATION": Column(
        int, Check.in_range(0, 6), nullable=False
    ),
    "MARRIAGE": Column(
        int, Check.in_range(0, 3), nullable=False
    ),
    "AGE": Column(
        int, Check.in_range(18, 100), nullable=False
    ),
    "DEFAULT_NEXT_MONTH": Column(
        int, Check.isin([0, 1]), nullable=False
    ),
}

# Validação dos códigos de atraso
for column in payment_delay_columns:
    columns[column] = Column(
        int,
        Check.in_range(-2, 8),
        nullable=False
    )

# Valores das faturas: negativos são permitidos
for column in bill_amount_columns:
    columns[column] = Column(
        int,
        nullable=False
    )

# Valores pagos: não podem ser negativos
for column in payment_amount_columns:
    columns[column] = Column(
        int,
        Check.ge(0),
        nullable=False
    )


credit_schema = pa.DataFrameSchema(
    columns,
    strict=True,
    coerce=False
)


def validate_credit_data(df):
    """
    Valida os dados de clientes de cartão de crédito.
    Retorna o DataFrame se todas as regras forem atendidas.
    """
    return credit_schema.validate(df)
