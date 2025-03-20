import pandas as pd
import vectorbt as vbt


def create_portfolio(df: pd.DataFrame, capital: float, freq: str) -> vbt.Portfolio:
    portfolio = vbt.Portfolio.from_signals(
        close=df["close"],
        entries=df["buy_signal"],
        exits=df["sell_signal"],
        init_cash=capital,
        freq=freq
    )
    return portfolio


def create_multi_asset_portfolio(df: pd.DataFrame, capital: float, freq: str) -> vbt.Portfolio:

    if not isinstance(df.index, pd.MultiIndex):
        raise ValueError("DataFrame index must be a MultiIndex with ('symbol', 'timestamp')")

    # Reshape (unstack symbols as columns)
    close = df["close"].unstack(level=0)  # Columns: symbols
    entries = df["buy_signal"].unstack(level=0)
    exits = df["sell_signal"].unstack(level=0)

    # Group symbols by their names
    group_by = close.columns  # This ensures correct length


    # Create portfolio
    portfolio = vbt.Portfolio.from_signals(
        close=close,
        entries=entries,
        exits=exits,
        init_cash=capital,
        freq=freq,
        group_by=group_by,  # Ensures correct length
        cash_sharing=True
    )

    return portfolio
