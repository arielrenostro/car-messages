import time
from datetime import datetime


def get_unix_timestamp(date_str: str) -> int:
    date = datetime.fromisoformat(date_str)
    return int(time.mktime(date.timetuple()))