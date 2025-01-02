from sqlite3 import Error as SqliteError
from src.utils import add_log


def main_exception_handler(func):
    def wrapper():
        try:
            func()
        except SqliteError as e:
            add_log(e)
        except BaseException as e:
            add_log(e)
    return wrapper
