from typing import Generator, Coroutine

from src.targets.target import Target


class FileReaderTarget(Target):

    def __init__(self, filepath: str, *args, **kwargs):
        self.filepath = filepath

        super().__init__(*args, **kwargs)

    def underlying(self, *args, **kwargs) -> Generator | Coroutine:
        with open(self.filepath, "r") as f:
            for line in f:
                self.target.run(line)
                yield
        self.target.close()

    def run(self, *args, **kwargs):
        self.gen_or_coro.send(None)
