import importlib
import inspect
import datetime as dt
from collections.abc import Generator, Coroutine, Iterator
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


def extract_data_from_coroutine(coro: Generator | Coroutine) \
        -> tuple[str, str, dict]:
    name, path = coro.gi_code.co_name, coro.gi_code.co_filename
    coro_params_names = inspect.Signature(coro).parameters.keys()
    params = {}
    for key, param in coro.gi_frame.f_locals.items():
        if key not in coro_params_names:
            continue
        params[key] = (
            extract_data_from_coroutine(param)
            if isinstance(param, Generator) or isinstance(param, Coroutine)
            else param
        )
    return name, path, params


def load_coro(name: str, path: str, params: dict):
    mod = importlib.import_module(name, path)
    func = getattr(mod, name)
    for key, param in params.items():
        if isinstance(param, dict):
            params[key] = load_coro(**param)
    return func(**params)
