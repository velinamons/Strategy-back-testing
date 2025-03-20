import pandas as pd
import vectorbt as vbt


def calculate_sma_rsi(df: pd.DataFrame, short_window: int = 10, long_window: int = 50, rsi_window: int = 14):
    df["SMA_short"] = vbt.MA.run(df["close"], window=short_window).ma
    df["SMA_long"] = vbt.MA.run(df["close"], window=long_window).ma
    df["RSI"] = vbt.RSI.run(df["close"], window=rsi_window).rsi
    return df


def calculate_sma_rsi_multi(df: pd.DataFrame, short_window: int = 10, long_window: int = 50, rsi_window: int = 14):
    df["SMA_short"] = df.groupby(level="symbol")["close"].transform(lambda x: vbt.MA.run(x, window=short_window).ma)
    df["SMA_long"] = df.groupby(level="symbol")["close"].transform(lambda x: vbt.MA.run(x, window=long_window).ma)
    df["RSI"] = df.groupby(level="symbol")["close"].transform(lambda x: vbt.RSI.run(x, window=rsi_window).rsi)
    return df


