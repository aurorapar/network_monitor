from enum import Enum, auto
import os
import pathlib

INTERFACE = 'Ethernet'
DATABASE_DIRECTORY = "saved_data"
DATABASE_FILENAME = "network_data.sqlite"
LOGGING_METHOD = "sqlite"


class LoggerMethod(Enum):
    SQLite = auto()


current_directory = pathlib.Path(__file__).parent.resolve()
SQLITE_DATABASE_LOCATION = os.path.join(current_directory, DATABASE_DIRECTORY, DATABASE_FILENAME)

if not os.path.exists(pathlib.Path(SQLITE_DATABASE_LOCATION).parent.resolve()):
    os.mkdir(pathlib.Path(SQLITE_DATABASE_LOCATION).parent.resolve())

for method in LoggerMethod:
    if str(method).lower().endswith(LOGGING_METHOD):
        LOGGING_METHOD = method

if type(LOGGING_METHOD) is str:
    raise RuntimeError("You did not specify a valid logging methods. Must match one of the values in LoggerMethod Enum")

