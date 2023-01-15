from uuid import uuid4
from enum import Enum
from typing import Optional, Any
from collections.abc import Generator, Coroutine
from abc import ABC, abstractmethod

from src.utils import string_to_timestamp


class JobStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    STARTED = 'STARTED'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'


class Job(ABC):
    def __init__(
        self,
        *,
        target: Optional["Job"] = None,
        start_at: str = "",
        max_working_time: int = -1,
        tries: int = 0,
        depends_on: list["Job"] = None
    ):
        self.job_id = str(uuid4())
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.target = target
        self.depends_on = depends_on or []
        self.priority = string_to_timestamp(self.start_at) \
            if self.start_at else 0
        self.status: JobStatus = JobStatus.NOT_STARTED
        self.parent_id: str | None = None
        self.gen_or_coro: Generator | Coroutine | None = None

    def run(self, data: Any = None):
        if self.status == JobStatus.NOT_STARTED:
            self.gen_or_coro = self.underlying()
        self.status = JobStatus.STARTED
        self.gen_or_coro.send(data)

    @abstractmethod
    def underlying(self, *args, **kwargs) -> Generator | Coroutine:
        raise NotImplementedError

    def stop(self) -> None:
        self.status = JobStatus.FINISHED
        if self.gen_or_coro:
            self.gen_or_coro.close()

    def to_json(self) -> dict:
        data = self.__dict__.copy()
        data["target"] = self.target.to_json() if self.target else None
        data["depends_on"] = [x.to_json() for x in self.depends_on]
        data["status"] = self.status.name
        return data

    @classmethod
    def from_json(cls, data: dict) -> "Job":
        data["status"] = JobStatus[data.get("status")]
        data["target"] = data.get("target", None)
        data["depends_on"] = [
            cls.from_json(x) for x in data.get("depends_on", [])
        ]
        return cls(**data)

    def __str__(self):
        return f"{self.job_id}"
