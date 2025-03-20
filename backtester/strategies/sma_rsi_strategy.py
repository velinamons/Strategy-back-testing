from typing import Dict

import pandas as pd

import vectorbt as vbt


def strategy_sma_rsi_single(df: pd.DataFrame, strategy_params: Dict):
    short_window = strategy_params.get("short_window", 20)
    long_window = strategy_params.get("long_window", 50)
    rsi_window = strategy_params.get("rsi_window", 14)
    rsi_buy = strategy_params.get("rsi_buy", 30)
    rsi_sell = strategy_params.get("rsi_sell", 70)

    df["SMA_short"] = vbt.MA.run(df["close"], window=short_window).ma
    df["SMA_long"] = vbt.MA.run(df["close"], window=long_window).ma
    df["RSI"] = vbt.RSI.run(df["close"], window=rsi_window).rsi

    df["buy_signal"] = (df["SMA_short"] > df["SMA_long"]) & (df["RSI"] < rsi_buy)
    df["sell_signal"] = (df["SMA_short"] < df["SMA_long"]) & (df["RSI"] > rsi_sell)

    return df


def strategy_sma_rsi_multi(df: pd.DataFrame, strategy_params: Dict):
    short_window = strategy_params.get("short_window", 20)
    long_window = strategy_params.get("long_window", 50)
    rsi_window = strategy_params.get("rsi_window", 14)
    rsi_buy = strategy_params.get("rsi_buy", 30)
    rsi_sell = strategy_params.get("rsi_sell", 70)

    df["SMA_short"] = df.groupby(level="symbol")["close"].transform(lambda x: vbt.MA.run(x, window=short_window).ma)
    df["SMA_long"] = df.groupby(level="symbol")["close"].transform(lambda x: vbt.MA.run(x, window=long_window).ma)
    df["RSI"] = df.groupby(level="symbol")["close"].transform(lambda x: vbt.RSI.run(x, window=rsi_window).rsi)

    # Generate buy/sell signals
    df["buy_signal"] = (df["SMA_short"] > df["SMA_long"]) & (df["RSI"] < rsi_buy)
    df["sell_signal"] = (df["SMA_short"] < df["SMA_long"]) & (df["RSI"] > rsi_sell)

    return df
