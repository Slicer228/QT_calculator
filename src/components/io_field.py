from PySide6.QtWidgets import QLineEdit, QMessageBox, QWidget, QApplication
from src.core.api import calculator_engine
from src.exceptions import InputSyntaxError


class FieldWidget(QWidget):
    _l_result = 0
    input_err_msg_box = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.line = QLineEdit('0', parent=self)
        self.input_err_msg_box = QMessageBox()
        self.input_err_msg_box.setText('Error in input!!!')

    def input(self, chars):
        try:
            calculator_engine.entry_string_to_expression(chars)
            self.line.setText(self.line.text() + chars)
        except InputSyntaxError:
            self.input_err_msg_box.exec()

    def update_input(self):
        for i, j in zip(self.line.text(), calculator_engine._expression):
            if i != j:
                self.input(i)

    def delete_left(self):
        self.line.backspace()
        calculator_engine.delete_last_chosen_element()

    def pass_result(self):
        self.line.setText(calculator_engine.get_result())



