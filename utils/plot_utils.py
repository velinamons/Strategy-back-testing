import os
from typing import List

import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import vectorbt as vbt

from settings import RESULTS_DIR


def create_multi_asset_result_plot(portfolio: vbt.Portfolio, portfolio_symbols: List[str]) -> go.Figure:
    """Creates a multi-asset result plot with orders, trade PnL, and cumulative returns."""

    n_symbols = len(portfolio_symbols)

    # Create subplots
    fig = make_subplots(
        rows=3, cols=n_symbols,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=[
            *[f"Orders - {symbol}" for symbol in portfolio_symbols],
            *[f"Trade PnL - {symbol}" for symbol in portfolio_symbols],
            *[f"Cumulative Returns - {symbol}" for symbol in portfolio_symbols]
        ],
    )

    for i, symbol in enumerate(portfolio_symbols, start=1):
        fig = _add_symbol_traces(fig, portfolio, symbol, i)

    fig.update_layout(
        height=900,
        width=n_symbols * 600,
        showlegend=True
    )

    return fig


def _add_symbol_traces(fig: go.Figure, portfolio: vbt.Portfolio, symbol: str, col: int) -> go.Figure:
    """Helper function to add traces for a specific symbol."""

    orders_plot = portfolio[symbol].plot_orders(fig=go.Figure())
    if col != 1:
        orders_plot.update_traces(showlegend=False)
    for trace in orders_plot.data:
        fig.add_trace(trace, row=1, col=col)

    # Trade PnL Plot
    trade_plot = portfolio[symbol].plot_trade_pnl(fig=go.Figure())
    if col != 1:
        trade_plot.update_traces(showlegend=False)
    for trace in trade_plot.data:
        fig.add_trace(trace, row=2, col=col)

    # Cumulative Returns Plot
    cum_returns_plot = portfolio[symbol].plot_cum_returns(fig=go.Figure())
    if col != 1:
        cum_returns_plot.update_traces(showlegend=False)
    for trace in cum_returns_plot.data:
        fig.add_trace(trace, row=3, col=col)

    return fig


# TODO: make normal path names
def save_plot_image(fig: go.Figure, symbols: list[str]) -> str:
    """Saves the given plot figure as a PNG image and returns the file path."""

    plot_path = os.path.join(RESULTS_DIR, f"{'_'.join(symbols)}_plot.png")
    pio.write_image(fig, plot_path, format="png")

    return plot_path


