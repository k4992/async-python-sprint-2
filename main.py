import argparse

from src.scheduler import Scheduler
from src.jobs.files import CreateFileJob, ReadFileJob, WriteFileJob


def main(state_filepath: str, restore: bool = False):
    scheduler = Scheduler()

    if restore:
        scheduler.restore_state(state_filepath)
    else:
        # write your own jobs and tasks
        file_creator_job = ReadFileJob(
            filepath="./log.txt",
            max_working_time=1,
            target=WriteFileJob(
                    max_working_time=1,
                    filepath="/Users/space_monkey/Desktop/tmp1.txt"
            ),
            depends_on=[
                CreateFileJob(
                    start_at="21:32",
                    filepath="/Users/space_monkey/Desktop/tmp1.txt",
                ),
                CreateFileJob(
                        start_at="21:37",
                        filepath="/Users/space_monkey/Desktop/tmp2.txt",
                ),
                CreateFileJob(
                        start_at="21:38",
                        filepath="/Users/space_monkey/Desktop/tmp3.txt",
                )
            ],
        )
        scheduler.schedule(file_creator_job)

    try:
        scheduler.run()
    except KeyboardInterrupt:
        scheduler.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Scheduler", description="Async Python: Sprint № 2"
    )
    parser.add_argument("-r", "--restore", action="store_true", default=False)
    parser.add_argument("-f", "--state-file", default="state.json")

    args = parser.parse_args()

    main(restore=args.restore, state_filepath=args.state_file)
