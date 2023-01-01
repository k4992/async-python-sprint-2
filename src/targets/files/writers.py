from typing import Generator, Coroutine

from src.targets.target import Target
from src.utils import coroutine


class FileWriterTarget(Target):

    def __init__(self, filepath: str, *args, **kwargs):
        self.filepath = filepath

        super().__init__(*args, **kwargs)

    def run(self, *args, **kwargs):
        self.gen_or_coro.send(*args, **kwargs)

    @coroutine
    def underlying(self, *args, **kwargs) -> Generator | Coroutine:
        with open(self.filepath, "w") as f:
            while line := (yield):
                f.write(line)
