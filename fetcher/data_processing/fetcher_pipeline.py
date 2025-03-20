from fetcher.data_processing import csv_proc, df_proc, zip_proc
from logger.config import logger
from utils import url_utils


async def process_daily_klines(symbol: str, date: str, interval: str) -> None:
    """
    Downloads Kline data for a single day.

    :param symbol: Trading pair symbol (e.g., 'BTCUSDT').
    :param date: Date in 'YYYY-MM-DD' format.
    :param interval: Kline interval (e.g., '1h', '5m').
    """
    try:
        zip_url = url_utils.build_zip_url(symbol, interval, date)
        zip_content = await zip_proc.download(zip_url)

        csv_data = zip_proc.extract_content(zip_content)

        raw_df = csv_proc.to_dataframe(csv_data)
        cleaned_df = df_proc.clean_data(raw_df)
        normalized_df = df_proc.normalize_data(cleaned_df)
        indexed_df = df_proc.set_index(normalized_df, symbol)

        df_proc.save_to_parquet(indexed_df, symbol, interval, date)

    except Exception as e:
        logger.error(f"Error processing {symbol} on {interval}, {date}: {e}")
