from src.db import db_engine
from src.exceptions_handler import main_exception_handler


@main_exception_handler
def main():
    print('started')
    db_engine.add_to_history([('',5),('add',5)],'10')
    print(next(db_engine.get_operations_history()))


if __name__ == '__main__':
    try:
        main()
    finally:
        db_engine.close()
