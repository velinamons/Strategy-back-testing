from datetime import date, datetime

import httpx

from fetcher.config import data_enums


from utils import url_utils
from utils.httpx_client import client, retry_on_httpx


@retry_on_httpx
async def async_validate_symbol(symbol: str) -> bool:
    """
    Asynchronously checks if the symbol exists by making a test request.
    :param symbol: Trading pair symbol (e.g., 'BTCUSDT').
    :return: True if the symbol is valid, otherwise False.
    """
    url = url_utils.build_symbol_url(symbol)

    try:
        response = await client.head(url)
        response.raise_for_status()
        return True
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return False
        raise


def validate_interval(interval):
    """Check if the interval is valid."""
    if interval not in data_enums.VALID_INTERVALS:
        raise ValueError(
            f"Invalid interval. Available intervals are: {', '.join(data_enums.VALID_INTERVALS)}."
        )
    return True


def validate_dates(start_date: date, end_date: date) -> None:
    """Validate start_date and end_date for correct format, logical order."""

    if start_date > end_date:
        raise ValueError(f"Start date can't be greater than end.")

    if end_date >= datetime.now().date():
        raise ValueError(f"End date can't be greater than the current date.")


def validate_date_range(
    start_date: str, end_date: str, valid_start: str, valid_end: str
):
    """
    Validates if the given start_date and end_date are within the allowed valid range.

    Args:
    - start_date: Start date input by the user (string in 'YYYY-MM-DD' format).
    - end_date: End date input by the user (string in 'YYYY-MM-DD' format).
    - valid_start: Valid start date (string in 'YYYY-MM-DD' format).
    - valid_end: Valid end date (string in 'YYYY-MM-DD' format).

    Returns:
    - (valid_start_date, valid_end_date): The validated start and end dates as strings.
    - Raises ValueError if the dates are invalid.
    """
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        valid_start = datetime.strptime(valid_start, "%Y-%m-%d").date()
        valid_end = datetime.strptime(valid_end, "%Y-%m-%d").date()

        if not (
            valid_start <= start_date <= valid_end
            and valid_start <= end_date <= valid_end
        ):
            raise ValueError("Date range out of bounds.")

        return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")

    except ValueError:
        raise ValueError(
            f"Invalid date range. Please provide a date range in the format 'YYYY-MM-DD'."
        )
