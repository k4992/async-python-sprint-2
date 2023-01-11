from uuid import uuid4
from enum import Enum
from typing import Generator, Coroutine

from src.utils import string_to_timestamp


class JobStatus(Enum):
    NOT_STARTED = 'NOT STARTED'
    STARTED = 'STARTED'
    PAUSED = 'PAUSED'
    FAILED = 'FAILED'
    FINISHED = 'FINISHED'


class Job:
    def __init__(
        self,
        *,
        target: Generator | Coroutine,
        start_at: str = "",
        max_working_time: int = -1,
        tries: int = 0,
        depends_on: list["Job"] = None,
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

    def run(self, *args, **kwargs):
        self.status = JobStatus.STARTED
        self.target.send(None)

    def pause(self) -> None:
        self.status = JobStatus.PAUSED
        pass

    def stop(self) -> None:
        self.status = JobStatus.FINISHED
        pass

    def __str__(self):
        return f"{self.job_id}"
