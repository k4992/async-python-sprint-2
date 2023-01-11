import pathlib
from typing import Generator, Coroutine

from src.utils import coroutine


def read_file(filepath: str, target: Coroutine) -> Generator:
    with open(filepath, "r") as f:
        for line in f:
            target.send(line)
            yield
    target.close()


def create_file(filepath: str) -> Generator:
    yield
    pathlib.Path(filepath).touch(mode=755, exist_ok=True)


@coroutine
def write_to_file(filepath: str) -> Coroutine:
    with open(filepath, "w") as f:
        while line := (yield):
            f.write(line)
