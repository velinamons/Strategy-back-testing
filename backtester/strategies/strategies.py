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

    df["buy_signal"] = (df["SMA_short"] > df["SMA_long"]) & (df["RSI"] < rsi_buy)
    df["sell_signal"] = (df["SMA_short"] < df["SMA_long"]) & (df["RSI"] > rsi_sell)

    return df


def strategy_macd_single(df: pd.DataFrame, strategy_params: Dict):
    short_window = strategy_params.get("short_window", 12)
    long_window = strategy_params.get("long_window", 26)
    signal_window = strategy_params.get("signal_window", 9)

    # Calculate MACD
    macd = vbt.MACD.run(df["close"], fast_window=short_window, slow_window=long_window, signal_window=signal_window)
    df["MACD"] = macd.macd
    df["MACD_signal"] = macd.signal

    df["buy_signal"] = df["MACD"] > df["MACD_signal"]
    df["sell_signal"] = df["MACD"] < df["MACD_signal"]

    return df


def strategy_macd_multi(df: pd.DataFrame, strategy_params: Dict):
    short_window = strategy_params.get("short_window", 12)
    long_window = strategy_params.get("long_window", 26)
    signal_window = strategy_params.get("signal_window", 9)

    df["MACD"] = df.groupby(level="symbol")["close"].transform(
        lambda x: vbt.MACD.run(x, fast_window=short_window, slow_window=long_window, signal_window=signal_window).macd
    )
    df["MACD_signal"] = df.groupby(level="symbol")["close"].transform(
        lambda x: vbt.MACD.run(x, fast_window=short_window, slow_window=long_window, signal_window=signal_window).signal
    )

    df["buy_signal"] = df["MACD"] > df["MACD_signal"]
    df["sell_signal"] = df["MACD"] < df["MACD_signal"]

    return df


def strategy_bollinger_bands_single(df: pd.DataFrame, strategy_params: Dict):
    window = strategy_params.get("window", 20)
    num_std = strategy_params.get("num_std", 2)

    bb = vbt.BBANDS.run(df["close"], window=window, alpha=num_std)
    df["BB_upper"] = bb.upper
    df["BB_lower"] = bb.lower
    df["BB_mid"] = bb.middle

    df["buy_signal"] = df["close"] < df["BB_lower"]
    df["sell_signal"] = df["close"] > df["BB_upper"]

    return df


def strategy_bollinger_bands_multi(df: pd.DataFrame, strategy_params: Dict):
    window = strategy_params.get("window", 20)
    num_std = strategy_params.get("num_std", 2)

    df["BB_upper"] = df.groupby(level="symbol")["close"].transform(
        lambda x: vbt.BBANDS.run(x, window=window, alpha=num_std).upper
    )
    df["BB_lower"] = df.groupby(level="symbol")["close"].transform(
        lambda x: vbt.BBANDS.run(x, window=window, alpha=num_std).lower
    )
    df["BB_mid"] = df.groupby(level="symbol")["close"].transform(
        lambda x: vbt.BBANDS.run(x, window=window, alpha=num_std).middle
    )

    df["buy_signal"] = df["close"] < df["BB_lower"]
    df["sell_signal"] = df["close"] > df["BB_upper"]

    return df


# TODO: Remove duplication
def strategy_stochastic_single(df: pd.DataFrame, strategy_params: Dict):
    k_window = strategy_params.get("k_window", 14)
    d_window = strategy_params.get("d_window", 3)
    stoch_buy = strategy_params.get("stoch_buy", 20)
    stoch_sell = strategy_params.get("stoch_sell", 80)

    stoch = vbt.STOCH.run(df["high"], df["low"], df["close"], k_window=k_window, d_window=d_window)
    df["%K"] = stoch.percent_k
    df["%D"] = stoch.percent_d

    df["buy_signal"] = (df["%K"] < stoch_buy) & (df["%K"] > df["%D"])
    df["sell_signal"] = (df["%K"] > stoch_sell) & (df["%K"] < df["%D"])

    return df


def strategy_stochastic_multi(df: pd.DataFrame, strategy_params: Dict):
    k_window = strategy_params.get("k_window", 14)
    d_window = strategy_params.get("d_window", 3)
    stoch_buy = strategy_params.get("stoch_buy", 20)
    stoch_sell = strategy_params.get("stoch_sell", 80)

    print(df.head(), df.columns, df.index.names)
    stoch = vbt.STOCH.run(df["high"], df["low"], df["close"], k_window=k_window, d_window=d_window)
    df["%K"] = stoch.percent_k
    df["%D"] = stoch.percent_d

    df["buy_signal"] = (df["%K"] < stoch_buy) & (df["%K"] > df["%D"])
    df["sell_signal"] = (df["%K"] > stoch_sell) & (df["%K"] < df["%D"])

    return df


def strategy_atr_breakout_single(df: pd.DataFrame, strategy_params: Dict):
    atr_window = strategy_params.get("atr_window", 14)
    atr_multiplier = strategy_params.get("atr_multiplier", 1.5)

    df["ATR"] = vbt.ATR.run(df["high"], df["low"], df["close"], window=atr_window).atr

    df["buy_signal"] = df["close"] > df["close"].shift(1) + (df["ATR"] * atr_multiplier)
    df["sell_signal"] = df["close"] < df["close"].shift(1) - (df["ATR"] * atr_multiplier)

    return df


def strategy_atr_breakout_multi(df: pd.DataFrame, strategy_params: Dict):
    atr_window = strategy_params.get("atr_window", 14)
    atr_multiplier = strategy_params.get("atr_multiplier", 1.5)

    df["ATR"] = vbt.ATR.run(df["high"], df["low"], df["close"], window=atr_window).atr

    df["buy_signal"] = df["close"] > df["close"].shift(1) + (df["ATR"] * atr_multiplier)
    df["sell_signal"] = df["close"] < df["close"].shift(1) - (df["ATR"] * atr_multiplier)

    return df
