from abc import ABC
from typing import Optional, Any, Generator, Coroutine


class Target(ABC):

    def __init__(self, target: Optional["Target"] = None, *args, **kwargs):
        self.target = target
        self.status = None
        self.gen_or_coro: Generator | Coroutine = self.underlying()

    def run(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    def underlying(self, *args, **kwargs) -> Generator | Coroutine:
        raise NotImplementedError

    def close(self) -> None:
        self.gen_or_coro.close()
