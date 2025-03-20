def build_zip_url(symbol: str, interval: str, date: str) -> str:
    """
    Builds the URL for downloading data from Binance.

    :param symbol: The trading symbol (e.g., 'BTCUSDT').
    :param interval: The interval for the data (e.g., '1h', '1s').
    :param date: The date in 'yyyy-mm-dd' format.
    :return: The URL for the data file.
    """
    return f"https://data.binance.vision/data/spot/daily/klines/{symbol}/{interval}/{symbol}-{interval}-{date}.zip"


def build_symbol_url(symbol: str) -> str:
    """
    Builds the symbol URL for checking symbol existence.

    :param symbol: The trading symbol (e.g., 'BTCUSDT').
    :return: The URL for the symbol.
    """
    return f"https://data.binance.vision/?prefix=data/spot/daily/klines/{symbol}/"

