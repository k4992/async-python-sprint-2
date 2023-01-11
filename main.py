from src.job import Job
from src.scheduler import Scheduler
from src.targets import (
    create_file, read_file, write_to_file)


if __name__ == "__main__":
    file_writer = write_to_file(
            filepath="/Users/space_monkey/Desktop/tmp1.txt")
    file_reader = read_file(filepath="./log.txt", target=file_writer)
    file_creator = create_file(
            filepath="/Users/space_monkey/Desktop/tmp1.txt")

    file_creator_job = Job(target=file_reader, depends_on=[
        Job(target=file_creator)
    ])

    scheduler = Scheduler()
    jobs = [file_creator_job]
    for job in jobs:
        scheduler.schedule(job)

    try:
        scheduler.run()
    except KeyboardInterrupt:
        scheduler.exit()
