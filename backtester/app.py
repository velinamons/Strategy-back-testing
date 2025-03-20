from datetime import datetime
from typing import List, Dict, Union
import pandas as pd

from logger.config import logger
from backtester.data_loader.parquet_loader import load_klines_range
from backtester.data_preprocessor.column_filter import drop_unused_columns
from backtester.portfolio import create_portfolio, create_multi_asset_portfolio
from backtester.strategies.sma_rsi_strategy import strategy_sma_rsi_single, strategy_sma_rsi_multi
from utils.path_utils import create_csv_path, create_plot_path
from utils.plot_utils import create_multi_asset_result_plot, save_multi_plot_image, save_single_plot_image
from utils.stats_utils import create_symbol_stats, save_stats_to_csv


async def run_backtest(
        asset: Union[str, List[str]],
        selected_interval: str,
        start_date: str,
        end_date: str,
        selected_strategy: str,
        strategy_params: Dict,
        portfolio_params: Dict
):

    """Runs a backtest for either single or multiple assets based on input type."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    logger.info(f"Backtest Starting for {asset} on range {start_date} - {end_date}, interval: {selected_interval}: {selected_strategy} with params: {strategy_params}")
    logger.info(f"Portfolio: {portfolio_params}")
    if isinstance(asset, list) and len(asset) > 0:
        return await run_backtest_multi(
            asset, selected_interval, start_date, end_date, selected_strategy, strategy_params, portfolio_params, timestamp
        )
    elif isinstance(asset, str):
        return await run_backtest_single(
            asset, selected_interval, start_date, end_date, selected_strategy, strategy_params, portfolio_params, timestamp
        )
    else:
        return {"error": "Invalid asset input. Must be a string or a non-empty list."}


async def run_backtest_single(
        symbol: str,
        interval: str,
        start_date: str,
        end_date: str,
        strategy_name: str,
        strategy_params: Dict,
        portfolio_params: Dict,
        timestamp: str
):
    """Runs a single-asset backtest and saves results."""

    df = load_klines_range(symbol=symbol, interval=interval, start_date=start_date, end_date=end_date)
    df = drop_unused_columns(df, ["close"])
    df = df.reset_index().set_index("timestamp").drop(columns=["symbol"])

    strategy_mapping = {
        "sma_rsi": strategy_sma_rsi_single
    }

    if strategy_name in strategy_mapping:
        df = strategy_mapping[strategy_name](df, strategy_params)
    else:
        return {"error": f"Strategy {strategy_name} not found"}

    portfolio = create_portfolio(df, portfolio_params, freq=interval)

    plot_path = create_plot_path([symbol], strategy_name, timestamp)
    save_single_plot_image(portfolio, plot_path)

    stats_path = create_csv_path([symbol], strategy_name, timestamp)
    symbol_stats = create_symbol_stats(portfolio)
    save_stats_to_csv(symbol_stats, stats_path)

    return {
        "result_path": stats_path,
        "plot_path": plot_path
    }


async def run_backtest_multi(
        symbols: List[str],
        interval: str,
        start_date: str,
        end_date: str,
        strategy_name: str,
        strategy_params: Dict,
        portfolio_params: Dict,
        timestamp: str
):
    """Runs a multi-asset backtest and saves results."""

    df_list = [load_klines_range(symbol=s, interval=interval, start_date=start_date, end_date=end_date) for s in symbols]
    df = pd.concat(df_list)

    df = drop_unused_columns(df, ["close"])

    strategy_mapping = {
        "sma_rsi": strategy_sma_rsi_multi
    }

    if strategy_name in strategy_mapping:
        df = strategy_mapping[strategy_name](df, strategy_params)
    else:
        return {"error": f"Strategy {strategy_name} not found"}

    portfolio = create_multi_asset_portfolio(df, portfolio_params, freq=interval)

    portfolio_symbols = portfolio.wrapper.columns.to_list()

    symbol_stats = create_symbol_stats(portfolio)
    stats_path = create_csv_path(portfolio_symbols, strategy_name, timestamp)
    save_stats_to_csv(symbol_stats, stats_path)

    plot_path = create_plot_path(portfolio_symbols, strategy_name, timestamp)
    plot_figure = create_multi_asset_result_plot(portfolio, portfolio_symbols)
    save_multi_plot_image(plot_figure, plot_path)

    return {
        "result_path": stats_path,
        "plot_path": plot_path
    }
