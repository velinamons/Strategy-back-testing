import pandas as pd

from fetcher.config import data_enums
from utils import path_utils


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the dataset by selecting relevant columns and converting data types.

    Args:
        df (pd.DataFrame): DataFrame to be cleaned.

    Returns:
        pd.DataFrame: DataFrame with only relevant columns and proper data types.
    """
    df.drop(columns=[col for col in df.columns if col not in data_enums.TARGET_COLUMNS], inplace=True)
    df = df.astype(data_enums.DTYPE_MAP, errors="ignore")

    return df


def get_time_unit(series: pd.Series) -> str:
    """Returns time_unit based on the most frequent length of integer values in the Series"""
    length_to_unit = {13: "ms", 16: "us"}

    len_series = series.apply(lambda x: len(str(x)))

    most_frequent_len = len_series.mode()[0]

    time_unit = length_to_unit.get(most_frequent_len, None)

    return time_unit


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes the dataset by handling missing data, interpolating datetime columns,
    and filling missing price and market activity values.

    Args:
        df (pd.DataFrame): DataFrame to be normalized.

    Returns:
        pd.DataFrame: DataFrame with interpolated and filled values.
    """

    for col in data_enums.DATETIME_COLUMNS:
        time_unit = get_time_unit(df[col])
        df[col] = pd.to_datetime(df[col], unit=time_unit, errors="coerce")

    df[data_enums.MARKET_ACTIVITY_COLUMNS] = df[data_enums.MARKET_ACTIVITY_COLUMNS].fillna(0)

    for col in data_enums.PRICE_COLUMNS:
        df[col] = df[col].replace(0, pd.NA)
        df[col] = df[col].ffill().bfill()

    return df


def set_index(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """
    Inserts the symbol as a new column at the beginning and sets the index.

    Args:
        df (pd.DataFrame): DataFrame to be modified.
        symbol (str): The symbol to be inserted.

    Returns:
        pd.DataFrame: DataFrame with the symbol column inserted and index set.
    """
    df.insert(0, "symbol", symbol)
    df.set_index(data_enums.INDEX_COLUMNS, inplace=True)
    return df


def save_to_parquet(df: pd.DataFrame, symbol: str, interval: str, date: str) -> str:
    """
    Saves a DataFrame to a compressed Parquet file using ZSTD compression.

    Args:
        df (pd.DataFrame): Processed DataFrame with MultiIndex.
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
        interval (str): Interval of klines (e.g., '1m', '1s', '5m').
        date (str): Date string in 'YYYY-MM-DD' format.

    Returns:
        str: Path to the saved Parquet file.
    """
    file_path = path_utils.create_parquet_path(symbol, interval, date)
    df.to_parquet(file_path, engine="pyarrow", index=True, compression="zstd")
    return file_path
