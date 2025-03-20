import os
from datetime import datetime

from settings import KLINES_DIR, RESULTS_DIR


def _construct_parquet_path(symbol: str, interval: str, date: str) -> tuple:
    """
    Constructs the Parquet file directory and filename.

    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
        interval (str): Interval of klines (e.g., '1m', '1s', '5m').
        date (str): Date string in 'YYYY-MM-DD' format.

    Returns:
        str: Full Parquet file path.
    """
    year, month, _ = date.split("-")
    file_dir = os.path.join(KLINES_DIR, symbol, year, month, interval)
    return file_dir, os.path.join(file_dir, f"{date}.parquet")


def create_parquet_path(symbol: str, interval: str, date: str) -> str:
    """
    Generates and ensures the Parquet file directory exists.

    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
        interval (str): Interval of klines (e.g., '1m', '1s', '5m').
        date (str): Date string in 'YYYY-MM-DD' format.

    Returns:
        str: Full Parquet file path.
    """
    file_dir, file_path = _construct_parquet_path(symbol, interval, date)
    os.makedirs(file_dir, exist_ok=True)
    return file_path


def get_parquet_path(symbol: str, interval: str, date: str) -> str:
    """
    Generates the Parquet file path without ensuring the directory exists.

    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
        interval (str): Interval of klines (e.g., '1m', '1s', '5m').
        date (str): Date string in 'YYYY-MM-DD' format.

    Returns:
        str: Full Parquet file path.
    """
    _, file_path = _construct_parquet_path(symbol, interval, date)
    return file_path


def _construct_plot_path(symbols: list[str], strategy_name: str) -> tuple:
    """
    Constructs the plot file directory and filename.

    Args:
        symbols (list[str]): List of trading symbols (e.g., ['BTCUSDT', 'ETHUSDT']).
        strategy_name (str): Name of the strategy used for the plot.

    Returns:
        tuple: Directory path and full plot file path.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # YYYYMMDD_HHMMSS_mmm
    filename = f"{'_'.join(symbols)}_{strategy_name}_{timestamp}.png"

    return RESULTS_DIR, os.path.join(RESULTS_DIR, filename)


def create_plot_path(symbols: list[str], strategy_name: str) -> str:
    """
    Generates and ensures the plot file directory exists.

    Args:
        symbols (list[str]): List of trading symbols (e.g., ['BTCUSDT', 'ETHUSDT']).
        strategy_name (str): Name of the strategy used for the plot.

    Returns:
        str: Full plot file path.
    """
    file_dir, file_path = _construct_plot_path(symbols, strategy_name)
    os.makedirs(file_dir, exist_ok=True)
    return file_path


def _construct_csv_path(symbols: list[str], strategy_name: str) -> tuple:
    """
    Constructs the CSV file directory and filename for backtest statistics.

    Args:
        symbols (list[str]): List of trading symbols (e.g., ['BTCUSDT', 'ETHUSDT']).
        strategy_name (str): Name of the strategy used for the backtest.

    Returns:
        tuple: Directory path and full CSV file path.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # YYYYMMDD_HHMMSS_mmm
    filename = f"{'_'.join(symbols)}_{strategy_name}_{timestamp}.csv"

    return RESULTS_DIR, os.path.join(RESULTS_DIR, filename)


def create_csv_path(symbols: list[str], strategy_name: str) -> str:
    """
    Generates and ensures the CSV file directory exists for backtest stats.

    Args:
        symbols (list[str]): List of trading symbols (e.g., ['BTCUSDT', 'ETHUSDT']).
        strategy_name (str): Name of the strategy used for the backtest.

    Returns:
        str: Full CSV file path.
    """
    file_dir, file_path = _construct_csv_path(symbols, strategy_name)
    os.makedirs(file_dir, exist_ok=True)
    return file_path