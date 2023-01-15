import json
from queue import PriorityQueue
from collections import defaultdict

from src.job import Job
from src.mixins import SingletonMeta


class Scheduler(metaclass=SingletonMeta):
    def __init__(self, pool_size: int = 10):
        self.pool_size = pool_size
        self.ready = PriorityQueue(maxsize=self.pool_size)
        self.waiting = defaultdict(list)
        self.available_jobs = {}

    def schedule(self, job: Job):
        main_job_id = job.job_id
        self.available_jobs[main_job_id] = job
        if not job.depends_on:
            self.ready.put(job)
            return

        for j in job.depends_on:
            j.parent_id = main_job_id
            self.waiting[main_job_id].append(j.job_id)
            self.available_jobs[j.job_id] = j

            if not j.depends_on:
                self.ready.put(j)
            else:
                self.schedule(j)

    def reschedule(self, job: Job):
        self.available_jobs[job.job_id] = job
        self.ready.put(job)

    def stop(self, job: Job):
        job.stop()
        del self.available_jobs[job.job_id]

        if job.parent_id and job.parent_id in self.waiting:
            self.waiting[job.parent_id].remove(job.job_id)
            if len(self.waiting[job.parent_id]) == 0:
                del self.waiting[job.parent_id]
                self.ready.put(self.available_jobs.get(job.parent_id))

    def run(self):
        while self.available_jobs:
            job: Job = self.ready.get()
            try:
                job.run()
            except StopIteration:
                self.stop(job)
                continue
            self.reschedule(job)

    def restore_state(self, filepath: str):
        with open(filepath, "r") as f:
            state = json.load(f)
        self.pool_size = state.get("pool_size", 10)
        self.waiting = defaultdict(list, state.get("waiting", {}))
        self.available_jobs = {
            job_id: Job.from_json(job) for job_id, job
            in state.get("available_jobs", {}).items()
        }
        self.ready = PriorityQueue(maxsize=self.pool_size)
        for job in [Job.from_json(x) for x in state.get("ready")]:
            self.schedule(job)

    def exit(self):
        state = dict(
                pool_size=self.pool_size,
                ready=[],
                available_jobs={},
                waiting=dict(self.waiting)
        )
        while type(self.ready) == PriorityQueue and not self.ready.empty():
            job = self.ready.get()
            state["ready"].append(job.to_json())

        for job_id, job in self.available_jobs.items():
            state["available_jobs"][job_id] = job.to_json()

        with open("state.json", "w") as f:
            json.dump(state, f)

        self.ready = PriorityQueue(maxsize=self.pool_size)
        self.waiting = defaultdict(list)
        self.available_jobs = {}
