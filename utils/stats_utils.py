import pandas as pd

from utils.path_utils import create_csv_path


def create_symbol_stats(portfolio) -> pd.DataFrame:
    """
    Creates the symbol statistics for the portfolio.

    Args:
        portfolio (Portfolio): The backtest portfolio.

    Returns:
        pd.DataFrame: The symbol stats as a DataFrame.
    """
    symbol_stats = portfolio.stats(agg_func=None)

    return symbol_stats


def save_stats_to_csv(symbol_stats: pd.DataFrame, path: str) -> None:
    symbol_stats.to_csv(path, index_label="Metric")
