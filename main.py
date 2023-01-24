import argparse

from src.scheduler import Scheduler
from src.utils import setup_logging
from src.jobs.files import CreateFileJob, ReadFileJob, WriteFileJob


def main(state_filepath: str, restore: bool = False):
    scheduler = Scheduler()

    if restore:
        scheduler.restore_state(state_filepath)
    else:
        # write your own jobs and tasks
        file_creator_job = ReadFileJob(
            filepath="./log.txt",
            tries=3,
            max_working_time=1,
            target=WriteFileJob(
                max_working_time=1, filepath="/Users/space_monkey/Desktop/tmp1.txt"
            ),
            depends_on=[
                CreateFileJob(
                    filepath="/Users/space_monkey/Desktop/tmp1.txt",
                ),
                # CreateFileJob(
                #         start_at="21:37",
                #         filepath="/Users/space_monkey/Desktop/tmp2.txt",
                # ),
                # CreateFileJob(
                #         start_at="21:38",
                #         filepath="/Users/space_monkey/Desktop/tmp3.txt",
                # )
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
    parser.add_argument("--log-config", default="logging.yml")

    args = parser.parse_args()

    setup_logging(logging_config_path=args.log_config)
    main(restore=args.restore, state_filepath=args.state_file)
