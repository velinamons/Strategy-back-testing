import pandas as pd

from backtester.strategies.indicators import calculate_sma_rsi, calculate_sma_rsi_multi


def strategy_sma_rsi_single(df: pd.DataFrame, rsi_buy: int = 30, rsi_sell: int = 70):
    df = calculate_sma_rsi(df)

    df["buy_signal"] = (df["SMA_short"] > df["SMA_long"]) & (df["RSI"] < rsi_buy)
    df["sell_signal"] = (df["SMA_short"] < df["SMA_long"]) & (df["RSI"] > rsi_sell)

    return df


def strategy_sma_rsi_multi(df: pd.DataFrame, rsi_buy: int = 30, rsi_sell: int = 70):
    df = calculate_sma_rsi_multi(df)

    df["buy_signal"] = (df["SMA_short"] > df["SMA_long"]) & (df["RSI"] < rsi_buy)
    df["sell_signal"] = (df["SMA_short"] < df["SMA_long"]) & (df["RSI"] > rsi_sell)

    return df
