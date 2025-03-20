from datetime import date, datetime

from settings import DATE_FORMAT


def date_from_string(date_str) -> date:
    return datetime.strptime(date_str, DATE_FORMAT).date()
