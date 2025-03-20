import os

import numpy as np
import pandas as pd
import plotly.io as pio
from plotly.subplots import make_subplots

from backtester.data_loader.parquet_loader import load_klines_range
from backtester.data_preprocessor.column_filter import drop_unused_columns
from backtester.portfolio import create_multi_asset_portfolio
from backtester.strategies.sma_rsi_strategy import strategy_sma_rsi_multi
from fetcher.config.data_enums import INDEX_COLUMNS
import plotly.graph_objects as go
from settings import RESULTS_DIR
from utils.plot_utils import create_multi_asset_result_plot, save_plot_image
from utils.stats_utils import create_symbol_stats, save_stats_to_csv


def run_backtest_multi(strategy_name: str, symbols: list[str], interval: str, start_date: str, end_date: str, capital: float):
    # Load data for all symbols
    df_list = [load_klines_range(symbol=s, interval=interval, start_date=start_date, end_date=end_date) for s in symbols]
    df = pd.concat(df_list)  # Combine into MultiIndex (symbol, timestamp)

    # Drop unused columns
    df = drop_unused_columns(df, ["close"])

    # TODO: create strategy choosing using dict
    if strategy_name == "sma_rsi":
        df = strategy_sma_rsi_multi(df)
    else:
        return f"Strategy {strategy_name} not found"

    # Create Multi-Asset Portfolio
    portfolio = create_multi_asset_portfolio(df, capital=capital, freq=interval)


    portfolio_symbols = portfolio.wrapper.columns.to_list()

    symbol_stats = create_symbol_stats(portfolio)
    stats_path = save_stats_to_csv(symbol_stats, portfolio_symbols, strategy_name)

    plot_figure = create_multi_asset_result_plot(portfolio, portfolio_symbols)
    plot_path = save_plot_image(plot_figure, portfolio_symbols)


    return {
        "result_path": RESULTS_DIR,
        "stats": portfolio.stats()
    }
