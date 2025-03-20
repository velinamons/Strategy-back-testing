from typing import List, Dict, Union
import pandas as pd

from backtester.data_loader.parquet_loader import load_klines_range
from backtester.data_preprocessor.column_filter import drop_unused_columns
from backtester.portfolio import create_portfolio, create_multi_asset_portfolio
from backtester.strategies.sma_rsi_strategy import strategy_sma_rsi_single, strategy_sma_rsi_multi
from utils.plot_utils import save_plot_image, create_multi_asset_result_plot
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

    if isinstance(asset, list) and len(asset) > 0:
        return await run_backtest_multi(
            asset, selected_interval, start_date, end_date, selected_strategy, strategy_params, portfolio_params
        )
    elif isinstance(asset, str):
        return await run_backtest_single(
            asset, selected_interval, start_date, end_date, selected_strategy, strategy_params, portfolio_params
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
        portfolio_params: Dict
):
    """Runs a single-asset backtest and saves results."""

    df = load_klines_range(symbol=symbol, interval=interval, start_date=start_date, end_date=end_date)
    df = drop_unused_columns(df, ["close"])
    df = df.reset_index().set_index("timestamp").drop(columns=["symbol"])


    strategy_mapping = {
        "sma_rsi": strategy_sma_rsi_single
    }

    if strategy_name in strategy_mapping:
        df = strategy_mapping[strategy_name](df, **strategy_params)
    else:
        return {"error": f"Strategy {strategy_name} not found"}

    portfolio = create_portfolio(df, portfolio_params, freq=interval)

    # Generate statistics and save results
    symbol_stats = create_symbol_stats(portfolio)
    stats_path = save_stats_to_csv(symbol_stats, [symbol], strategy_name)

    plot_figure = create_result_plot(portfolio, [symbol])
    plot_path = save_plot_image(plot_figure, [symbol])

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
        portfolio_params: Dict
):
    """Runs a multi-asset backtest and saves results."""

    df_list = [load_klines_range(symbol=s, interval=interval, start_date=start_date, end_date=end_date) for s in
               symbols]
    df = pd.concat(df_list)  # Combine into MultiIndex (symbol, timestamp)

    df = drop_unused_columns(df, ["close"])


    strategy_mapping = {
        "sma_rsi": strategy_sma_rsi_multi
    }

    if strategy_name in strategy_mapping:
        df = strategy_mapping[strategy_name](df, **strategy_params)
    else:
        return {"error": f"Strategy {strategy_name} not found"}

    # Create Multi-Asset Portfolio
    portfolio = create_multi_asset_portfolio(df, portfolio_params, freq=interval)

    portfolio_symbols = portfolio.wrapper.columns.to_list()

    # Generate statistics and save results
    symbol_stats = create_symbol_stats(portfolio)
    stats_path = save_stats_to_csv(symbol_stats, portfolio_symbols, strategy_name)

    plot_figure = create_multi_asset_result_plot(portfolio, portfolio_symbols)
    plot_path = save_plot_image(plot_figure, portfolio_symbols)

    return {
        "result_path": stats_path,
        "plot_path": plot_path
    }
