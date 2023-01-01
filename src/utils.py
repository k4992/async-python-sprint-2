import datetime as dt
from functools import wraps


TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"


def coroutine(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        coro = f(*args, **kwargs)
        next(coro)
        return coro
    return wrapped


def string_to_timestamp(date_as_str: str) -> float:
    formats = [DATETIME_FORMAT, TIME_FORMAT]
    value = None
    for _format in formats:
        try:
            value = dt.datetime.strptime(date_as_str, _format)
            if _format == TIME_FORMAT:
                value = dt.datetime.combine(dt.date.today(), value.time())
        except ValueError:
            pass

    if value is None:
        raise ValueError(
            f"Failed to convert {date_as_str} to datetime. Allowed formats are {formats}."
        )
    return value.timestamp()
