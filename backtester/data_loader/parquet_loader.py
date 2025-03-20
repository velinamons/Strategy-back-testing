import os
import pandas as pd
from typing import List

from settings import DATE_FORMAT
from utils import path_utils


def load_daily_klines(symbol: str, interval: str, date: str) -> pd.DataFrame:
    """
    Loads Parquet data for a single day.

    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
        interval (str): Interval of klines (e.g., '1m', '1h', '1d').
        date (str): Date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: DataFrame for the requested day.
    """
    file_path = path_utils.get_parquet_path(symbol, interval, date)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Parquet file not found: {file_path}")

    return pd.read_parquet(file_path)


def load_klines_range(symbol: str, interval: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Loads multiple days of Parquet data into a single DataFrame.

    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
        interval (str): Interval of klines (e.g., '1m', '1h', '1d').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: Merged DataFrame containing requested data.
    """
    date_range = pd.date_range(start=start_date, end=end_date, freq="D")
    data_frames: List[pd.DataFrame] = []

    for date in date_range:
        date_str = date.strftime(DATE_FORMAT)

        day_df = load_daily_klines(symbol, interval, date_str)

        data_frames.append(day_df)

    return pd.concat(data_frames).sort_index()
