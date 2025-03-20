import pandas as pd
from typing import List


def drop_unused_columns(df: pd.DataFrame, required_columns: List[str]) -> pd.DataFrame:
    """
    Drops unused columns from the DataFrame, keeping only the required ones.

    Args:
        df (pd.DataFrame): The input DataFrame containing kline data.
        required_columns (List[str]): The list of columns needed for a strategy.

    Returns:
        pd.DataFrame: The DataFrame with only the required columns.
    """
    return df[required_columns].copy()
