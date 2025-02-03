import sys
from src.db import db_engine
from src.exceptions_handler import main_exception_handler
import src.page
from PySide6.QtWidgets import QApplication, QLabel,QPushButton
from src.components.io_field import FieldWidget


@main_exception_handler
def main():
    app = QApplication(sys.argv)
    fw = FieldWidget()
    fw.show()
    btn1 = QPushButton('=')
    btn1.clicked.connect(fw.pass_result)
    btn2 = QPushButton('-')
    btn2.clicked.connect(lambda: fw.input('-'))
    btn3 = QPushButton('upd')
    btn3.clicked.connect(lambda: fw.update_input())
    btn1.show()
    btn2.show()
    btn3.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    try:
        main()
    finally:
        db_engine.close()
