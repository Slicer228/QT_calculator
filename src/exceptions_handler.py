from sqlite3 import Error as SqliteError
from src.utils import add_log
from src.exceptions import InputSyntaxError


def main_exception_handler(func):
    def wrapper():
        try:
            func()
        except SqliteError as e:
            add_log(e)
        except InputSyntaxError:
            print('Input Error!')
        except BaseException as e:
            add_log(e)
    return wrapper
