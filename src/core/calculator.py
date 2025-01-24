from src.core.expression import CalculatorExpressionHandler
from src.schemas import SingleOperationSchema, GroupOperationSchema


class Calculator(CalculatorExpressionHandler):
    _current_calculation = None
    _MAX_PRIORITY = 5

    def get_result(self):
        self._current_calculation = self._queue
        priority = 1
        while len(self._queue) > 1 or self._queue[0].operation.priority != 0:
            for _index, _i in enumerate(self._current_calculation):
                if len(self._current_calculation) == 1:
                    priority = 1
                    self._current_calculation = self._queue
                    break
                if isinstance(_i, GroupOperationSchema):
                    if len(_i) == 1:
                        self._current_calculation[_index] = self._convert_group_to_operation(_i, _i[0].value)
                        break
                    else:
                        self._current_calculation = _i
                        break
                elif isinstance(_i, SingleOperationSchema):
                    if priority == _i:
                        self._calculate_operation(_index)
                        priority = 1
                        break
                if _index == len(self._current_calculation) - 1:
                    priority += 1
                    if priority > self._MAX_PRIORITY:
                        priority = 1
                        self._current_calculation = self._queue
                        break
        return self._queue[0].value if isinstance(self._queue[0], SingleOperationSchema) else 0


    def _calculate_operation(self,index):
        if isinstance(self._current_calculation[index].operation, tuple):
            self._current_calculation[index].value = self._current_calculation[index].operation[1].executable(
                self._current_calculation[index].value
            )
            self._current_calculation[index - 1].value = self._current_calculation[index].operation[0].executable(
                self._current_calculation[index - 1].value,
                self._current_calculation[index].value
            )
            self._current_calculation.pop(index)
        else:
            if self._current_calculation[index].operation.priority == 0:
                pass
            elif self._current_calculation[index].operation.priority == 1:
                self._current_calculation[index].value = self._current_calculation[index].operation.executable(
                    self._current_calculation[index].value,
                )
                self._current_calculation[index].operation.priority = 0
                self._current_calculation[index].operation.perfomance = ''
            else:
                self._current_calculation[index-1].value = self._current_calculation[index].operation.executable(
                    self._current_calculation[index-1].value,
                    self._current_calculation[index].value
                )
                self._current_calculation.pop(index)