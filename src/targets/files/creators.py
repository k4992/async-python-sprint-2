import pathlib
from typing import Generator, Coroutine

from src.targets.target import Target


class FileCreatorTarget(Target):

    def __init__(self, filepath: str, *args, **kwargs):
        self.filepath = filepath

        super().__init__(*args, **kwargs)

    def underlying(self, *args, **kwargs) -> Generator | Coroutine:
        pathlib.Path(self.filepath).touch(mode=755, exist_ok=True)
        yield

    def run(self, *args, **kwargs):
        self.gen_or_coro.send(None)
