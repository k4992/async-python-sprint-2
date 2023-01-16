class TimeLimitExceededException(Exception):
    def __init__(self, message="Time limit has exceeded"):
        super().__init__(message)
