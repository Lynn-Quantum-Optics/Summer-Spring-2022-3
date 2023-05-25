import datetime
import os
from functools import wraps

from Enums import RecordType


class Logger:
    log_file = None

    def __init__(self, config):
        self._config = config

        now = datetime.datetime.now()
        date_string = now.strftime("%m-%d-%Y_%H-%M-%S")
        self.log_name = f"{date_string}__log"

        os.makedirs(f"{config.log_directory}", exist_ok=True)
        Logger.log_file = open(f"{config.log_directory}/{self.log_name}.csv", 'w')

        self.initialize_log_file()

    def initialize_log_file(self):
        # may prefer to format the names without a newline in between each
        contributors_string = ',\n'.join(self._config.contributors)

        Logger.log_file.writelines([
            f"{self._config.title}\n",
            f"Time Stamp: {datetime.datetime.today()}.\n",
            f"Contributors:\n{contributors_string}\n",
            f"=============LOG START=============\n"
            f"time stamp, record type, message\n"
        ])
        Logger.log_file.flush()

    @staticmethod
    def log(record_type, message):
        if Logger.log_file:
            now = datetime.datetime.now()
            date_string = now.strftime("%m-%d-%Y_%H-%M-%S")
            Logger.log_file.writelines([
                # this time stamp should be updated to exclude the month, day, year
                f"{date_string}, {record_type.name}, {message}\n"
            ])
            Logger.log_file.flush()
        else:
            raise Exception("Tried to log a record before Logger initialized.")

    @staticmethod
    def log_wrap(func=None, function_name_override=None):

        @wraps(func)
        def inner(*args, **kwargs):
            try:
                if function_name_override:
                    Logger.log(RecordType.Call, f"Calling Function: {function_name_override}")
                else:
                    Logger.log(RecordType.Call, f"Calling Function: {func.__name__}")
                Logger.log(RecordType.Detail, f"Args: {args}")
                for kwarg in kwargs:
                    Logger.log(RecordType.Detail, f"{kwarg}: {kwargs[kwarg]}")
                response = func(*args, **kwargs)
                Logger.log(RecordType.Return, f"{func.__name__} Returned: {response}")
                return response
            except Exception as exc:
                Logger.log(RecordType.Error, f"{exc}")
                raise exc

        return inner
