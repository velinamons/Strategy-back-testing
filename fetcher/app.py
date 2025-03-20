import asyncio
from datetime import timedelta

from fetcher.data_processing import fetcher_pipeline
from logger.config import logger
from settings import DATE_FORMAT, SYMBOLS_CONFIG
from utils import date_utils, validators


async def fetch_klines_batch():
    """
    Fetch klines data for all symbols and intervals from SYMBOLS_CONFIG before running the bot.
    """

    logger.info("Starting kline data fetching for symbols")
    tasks = []
    for symbol, intervals in SYMBOLS_CONFIG.items():
        for interval, date_range in intervals.items():
            start_date = date_range["start_date"]
            end_date = date_range["end_date"]
            tasks.append(fetch_klines_for_symbol(symbol, start_date, end_date, interval))

    if tasks:
        await asyncio.gather(*tasks)
        logger.info("Finished fetching kline data")
    else:
        logger.warning("No kline data tasks to fetch")


async def fetch_klines_for_symbol(symbol: str, start_date: str, end_date: str, interval: str) -> None:
    """
    Function to download, preprocess, and store Binance market data for a date range.

    :param symbol: Trading pair symbol (e.g., 'BTCUSDT').
    :param start_date: Start date in 'YYYY-MM-DD' format.
    :param end_date: End date in 'YYYY-MM-DD' format.
    :param interval: Kline interval (e.g., '1h', '5m').
    """
    logger.info(f"Start loading data for {symbol} on {interval}, start: {start_date}, end: {end_date}")
    try:
        await validators.async_validate_symbol(symbol)
        validators.validate_interval(interval)
        start_date = date_utils.date_from_string(start_date)
        end_date = date_utils.date_from_string(end_date)
        validators.validate_dates(start_date, end_date)

        tasks = []
        current_date = start_date
        while current_date <= end_date:
            tasks.append(fetcher_pipeline.process_daily_klines(symbol, current_date.strftime(DATE_FORMAT), interval))
            current_date += timedelta(days=1)
        await asyncio.gather(*tasks)
        logger.info(f"Parquet files created for {symbol} on {interval}, start: {start_date}, end: {end_date}")
    except ValueError as e:
        logger.error(f"Error validating {symbol} on {interval}, start: {start_date}, end: {end_date}: {e}")
    except Exception as e:
        logger.error(f"Error {symbol} on {interval}: {e}")
