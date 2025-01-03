from src.db import db_engine
from src.exceptions_handler import main_exception_handler


@main_exception_handler
def main():
    print('started')


if __name__ == '__main__':
    try:
        main()
    finally:
        db_engine.close()
