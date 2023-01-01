from src.job import Job
from src.scheduler import Scheduler
from src.targets import FileReaderTarget, FileWriterTarget, FileCreatorTarget


if __name__ == "__main__":
    file_writer = FileWriterTarget(
            filepath="/Users/space_monkey/Desktop/tmp1.txt")
    file_reader = FileReaderTarget(filepath="./log.txt", target=file_writer)
    file_creator = FileCreatorTarget(
            filepath="/Users/space_monkey/Desktop/tmp1.txt")

    file_creator_job = Job(target=file_reader, depends_on=[
        Job(target=file_creator)
    ])

    scheduler = Scheduler()
    jobs = [file_creator_job]
    for job in jobs:
        scheduler.schedule(job)
    scheduler.run()
