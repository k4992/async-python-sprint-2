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
        job_id: str | None = None,
        parent_id: str | None = None,
        priority: int | None = None,
        target: Optional["Job"] = None,
        start_at: str = "",
        max_working_time: int = -1,
        tries: int = 0,
        depends_on: list["Job"] = None
    ):
        self.job_id = job_id if job_id else str(uuid4())
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.target = target
        self.depends_on = depends_on or []
        self.priority = self.__get_priority(
                priority=priority, start_at=start_at)
        self.status: JobStatus = JobStatus.NOT_STARTED
        self.parent_id: str | None = parent_id
        self.gen_or_coro: Generator | Coroutine | None = None

    @staticmethod
    def __get_priority(
            priority: int | None = None,
            start_at: str = ""
    ) -> int | float:
        if priority is not None:
            return priority
        if start_at:
            return string_to_timestamp(start_at)
        return 0

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

        data.pop("status")
        data.pop("gen_or_coro")

        data["target"] = self.target.to_json() if self.target else None
        data["depends_on"] = [x.to_json() for x in self.depends_on]
        data["class_name"] = self.__class__.__name__
        return data

    def __str__(self):
        return f"{self.job_id}"
