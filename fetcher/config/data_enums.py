from typing import Dict, List

# TODO: enums

CSV_COLUMNS: List[str] = [
    "timestamp", "open", "high", "low", "close", "volume",
    "close_time", "quote_asset_volume", "trades",
    "taker_buy_base", "taker_buy_quote", "ignore"
]

DTYPE_MAP: Dict[str, str] = {
    "timestamp": "int64",
    "open": "float64",
    "high": "float64",
    "low": "float64",
    "close": "float64",
    "volume": "float64",
    "close_time": "int64",
    "quote_asset_volume": "float64",
    "trades": "int32",
    "taker_buy_base": "float64",
    "taker_buy_quote": "float64",
}

TARGET_COLUMNS: List[str] = list(DTYPE_MAP.keys())

INDEX_COLUMNS: List[str] = [
    "symbol",
    "timestamp"
]

DATETIME_COLUMNS: List[str] = [
    "timestamp",
    "close_time"
]

PRICE_COLUMNS: List[str] = [
    "open",
    "high",
    "low",
    "close"
]

MARKET_ACTIVITY_COLUMNS: List[str] = [
    "volume",
    "quote_asset_volume",
    "trades",
    "taker_buy_base",
    "taker_buy_quote"
]

VALID_INTERVALS: List[str] = [
    "1s",
    "1m",
    "3m",
    "5m",
    "15m",
    "30m",
    "1h",
    "2h",
    "4h",
    "6h",
    "8h",
    "12h",
]
