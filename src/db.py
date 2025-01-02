import sqlite3
import json
from src.schemas import OperationPageSchema
from src.config_engine import app_config


PAGINATION_HISTORY_LIMIT = int(app_config.main.pagination_history_limit.text)


class Connection(sqlite3.Connection):
    def __init__(self, db):
        super().__init__(db)
        self.cursor = self.cursor()
        self.__existing_check()

    def __existing_check(self):
        query = """
        CREATE TABLE IF NOT EXISTS operations_history(
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            operation TEXT NOT NULL,
            RESULT TEXT NOT NULL
        )
        """
        self.cursor.execute(query)

    def get_operations_history(self) -> object | list[object]:
        fetches = 0
        while True:
            query = f"""
                SELECT * FROM operations_history
                LIMIT {PAGINATION_HISTORY_LIMIT}
                OFFSET {PAGINATION_HISTORY_LIMIT * fetches}
            """
            ops = self.cursor.execute(query).fetchall()
            ops = [OperationPageSchema(time=i[0],
                                       operation=json.loads(i[1]),
                                       result=i[2])
                   for i in ops]
            if len(ops) < PAGINATION_HISTORY_LIMIT:
                break
            else:
                fetches += 1
                yield ops

        yield ops

    def add_to_history(self, operation: str, result: str):
        query = f"""
            INSERT INTO operations_history(operation, result)
            VALUES('{json.dumps(operation)}','{result}')
        """
        self.cursor.execute(query)
        self.commit()


db_engine = Connection('app.db')
