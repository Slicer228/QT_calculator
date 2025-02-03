from src.convert_input import sheet
from src.schemas import SingleOperationSchema, GroupOperationSchema
from src.exceptions import InputSyntaxError


class CalculatorQueryHandler:
    _ALLOWED_SOLO_OPERATIONS = ['!', 'empty']
    _queue = []
    _groups_deep_len = 0
    _current_group = _queue

    def _add_group_to_queue(self, operation='empty'):
        if len(self._current_group) == 0 and operation not in self._ALLOWED_SOLO_OPERATIONS:
            raise InputSyntaxError
        if len(self._current_group) > 0 and operation in self._ALLOWED_SOLO_OPERATIONS:
            raise InputSyntaxError
        self._current_group.append(GroupOperationSchema(
            operation=sheet[operation],
            group=[]
        ))
        self._groups_deep_len += 1
        self._current_group = self._current_group[-1].group

    def _end_group(self):
        self._groups_deep_len = self._groups_deep_len - 1 if self._groups_deep_len >= 1 else 0
        self._go_to_current_new_group()

    def _add_operation(self, value, operation='empty'):
        if len(self._current_group) == 0 and operation not in self._ALLOWED_SOLO_OPERATIONS:
            raise InputSyntaxError
        if len(self._current_group) > 0 and operation in self._ALLOWED_SOLO_OPERATIONS:
            raise InputSyntaxError
        self._current_group.append(SingleOperationSchema(
            operation=sheet[operation],
            value=value
        ))

    def _add_double_operation_group(self, operation, solo_operation):
        if len(self._current_group) == 0:
            raise InputSyntaxError
        self._current_group.append(GroupOperationSchema(
            operation=(sheet[operation], sheet[solo_operation]),
            group=[]
        ))
        self._groups_deep_len += 1
        self._current_group = self._current_group[-1].group

    def _add_double_operation(self, operation, solo_operation, value):
        if len(self._current_group) == 0:
            raise InputSyntaxError
        self._current_group.append(SingleOperationSchema(
            operation=(sheet[operation], sheet[solo_operation]),
            value=value
        ))

    def delete_last_chosen_element(self):
        if self._queue:
            if len(self._current_group) == 0:
                self._groups_deep_len -= 1
                self._go_to_current_new_group()
                self._current_group.pop()
            else:
                self._current_group.pop()

    def _go_to_current_new_group(self):
        if self._queue:
            self._current_group = self._queue[-1].group if self._groups_deep_len else self._queue
            for _i in range(self._groups_deep_len - 1):
                self._current_group = self._current_group[-1].group

    def _clear_queue(self):
        self._groups_deep_len = 0
        del self._queue[:]
        self._current_group = self._queue

    def _print_group(self, group):
        print('(', end='')
        for _i in group:
            if isinstance(_i, SingleOperationSchema):
                print(_i.operation.perfomance \
                      if not isinstance(_i.operation, tuple) \
                      else _i.operation[0].perfomance + ' ' + _i.operation[1].perfomance,
                      _i.value,
                      end=' ',
                      sep='')
            else:
                print(
                    _i.operation.perfomance \
                    if not isinstance(_i.operation, tuple) \
                    else _i.operation[0].perfomance + ' ' + _i.operation[1].perfomance,
                    end='')
                self._print_group(_i.group)
        print(')', end='')

    def _print_queue(self):
        self._print_group(self._queue)

    @staticmethod
    def _convert_group_to_operation(self, group, result):
        return SingleOperationSchema(
            operation=group.operation,
            value=result
        )
