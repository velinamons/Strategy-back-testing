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
    # Get stats without aggregation
    symbol_stats = portfolio.stats(agg_func=None)

    return symbol_stats


def save_stats_to_csv(symbol_stats: pd.DataFrame, symbols: list[str], strategy_name: str) -> str:
    """
    Saves the backtest statistics to a CSV file.

    Args:
        symbol_stats (pd.DataFrame): The DataFrame containing the backtest stats.
        symbols (list[str]): List of trading symbols (e.g., ['BTCUSDT', 'ETHUSDT']).
        strategy_name (str): Name of the strategy used for the backtest.

    """
    stats_file = create_csv_path(symbols, strategy_name)
    symbol_stats.to_csv(stats_file, index_label="Metric")

    return stats_file
