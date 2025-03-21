import pandas as pd
import vectorbt as vbt


# TODO: add portfolio param 'size'
def create_portfolio(df: pd.DataFrame, portfolio_params: dict, freq: str) -> vbt.Portfolio:
    portfolio = vbt.Portfolio.from_signals(
        close=df["close"],
        entries=df["buy_signal"],
        exits=df["sell_signal"],
        freq=freq,
        **portfolio_params
    )
    return portfolio


def create_multi_asset_portfolio(df: pd.DataFrame, portfolio_params: dict, freq: str) -> vbt.Portfolio:

    if not isinstance(df.index, pd.MultiIndex):
        raise ValueError("DataFrame index must be a MultiIndex with ('symbol', 'timestamp')")

    close = df["close"].unstack(level=0)
    entries = df["buy_signal"].unstack(level=0)
    exits = df["sell_signal"].unstack(level=0)

    group_by = close.columns

    portfolio = vbt.Portfolio.from_signals(
        close=close,
        entries=entries,
        exits=exits,
        freq=freq,
        group_by=group_by,
        cash_sharing=True,
        **portfolio_params
    )

    return portfolio
