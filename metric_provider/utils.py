from datetime import datetime
from decimal import Decimal


def get_unix_timestamp(date_str: str) -> int:
    date = convert_date_to_str(date_str)
    unix = int(
        date.timestamp() * 1000  # Must be in milliseconds
    )
    return unix


def convert_date_to_str(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y/%m/%dT%H:%M:%S.%fZ")
    except:
        return datetime.strptime(date_str, "%Y/%m/%dT%H:%M:%SZ")


def decimal_encoder(o):
    if isinstance(o, Decimal):
        return float(o)
    raise TypeError(repr(o) + " is not JSON serializable")
