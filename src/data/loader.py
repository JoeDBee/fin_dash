import datetime as dt
from functools import partial, reduce
from typing import Callable

import babel.dates
import i18n
import pandas as pd

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(str)
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df[DataSchema.MONTH] = df[DataSchema.DATE].dt.month.astype(str)
    return df


def translate_date(df: pd.DataFrame, locale: str) -> pd.DataFrame:
    def date_repr(date: dt.date) -> str:
        return babel.dates.format_date(date, format="MMMM", locale=locale)

    df[DataSchema.MONTH] = df[DataSchema.DATE].apply(date_repr)
    return df


def translate_category(df: pd.DataFrame) -> pd.DataFrame:
    def translate(category: str) -> str:
        return i18n.t(f"category.{category}")

    df[DataSchema.CATEGORY] = df[DataSchema.CATEGORY].apply(translate)
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    # Nested lambda: given f, g, and x, compute g(f(x))
    # reduce: reduce iterable to single value by cumulatively applying given function
    # Together: apply composition of functions to x
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def load_transaction_data(path: str, locale: str) -> pd.DataFrame:
    # load the data from a CSV file
    data = pd.read_csv(
        path,
        dtype={
            DataSchema.AMOUNT: float,
            DataSchema.CATEGORY: str
        },
        parse_dates=[DataSchema.DATE]
    )
    preprocessor = compose(
        create_year_column,
        create_month_column,
        partial(translate_date, locale=locale),
        translate_category
    )
    return preprocessor(data)

