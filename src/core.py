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

    def _delete_last_chosen_element(self):
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

    def _convert_group_to_operation(self, group, result):
        return SingleOperationSchema(
            operation=group.operation,
            value=result
        )


class CalculatorExpressionHandler(CalculatorQueryHandler):
    _ALLOWED_OPERATIONS = ['+', '-', '*', '/']
    _ALLOWED_NUMBERS = [str(_i) for _i in range(0, 10)]
    _got_operation = True
    _expression = ''

    def _verify_symbol(self, s):
        if s in self._ALLOWED_OPERATIONS \
                or s in self._ALLOWED_NUMBERS \
                or s in self._ALLOWED_SOLO_OPERATIONS \
                or s in ('(', ')'):
            return True
        return False

    def entry_string_to_expression(self, string):
        string = string.strip()
        for s in string:
            self.entry_to_expression(s)

    def entry_to_expression(self, symbol):
        if not self._verify_symbol(symbol):
            raise InputSyntaxError
        if self._got_operation:
            if symbol == '(':
                if self._groups_deep_len == 0 and symbol == ')':
                    raise InputSyntaxError
                self._expression += symbol
                self._parse_backwards_and_add()
            elif symbol in self._ALLOWED_NUMBERS \
                    or symbol in self._ALLOWED_SOLO_OPERATIONS:
                if len(self._expression) > 0:
                    if self._expression[-1] in self._ALLOWED_SOLO_OPERATIONS and symbol in self._ALLOWED_SOLO_OPERATIONS:
                        raise InputSyntaxError
                self._expression += symbol
                self._parse_backwards_and_add()
                if symbol in self._ALLOWED_NUMBERS:
                    self._got_operation = False
            else:
                raise InputSyntaxError
        else:
            if symbol == ')':
                self._expression += symbol
                self._parse_backwards_and_add()
            elif symbol in self._ALLOWED_OPERATIONS:
                self._got_operation = True
                self._expression += symbol
            elif symbol in self._ALLOWED_NUMBERS:
                self._expression += symbol
                self._parse_backwards_and_add()
            else:
                raise InputSyntaxError

    def _parse_backwards_and_add(self):
        if len(self._expression) == 0:
            return None
        value_tmp = ''
        reversed_expression = self._expression[::-1]
        index = 0
        if reversed_expression[index] == ')':
            self._end_group()
        elif reversed_expression[index] == '(':
            if len(self._expression) == 1:
                self._add_group_to_queue()
            elif len(self._expression) >= 3 and reversed_expression[index + 2] in self._ALLOWED_OPERATIONS:
                self._add_double_operation_group(reversed_expression[index + 2], reversed_expression[index + 1])
            else:
                self._add_group_to_queue(reversed_expression[index + 1])
        elif reversed_expression[index] in self._ALLOWED_NUMBERS:
            while reversed_expression[index] in self._ALLOWED_NUMBERS:
                value_tmp += reversed_expression[index]
                if index + 1 == len(reversed_expression):
                    index += 1
                    break
                index += 1
            if len(value_tmp) > 1:
                self._delete_last_chosen_element()
            if len(self._expression) == index or reversed_expression[index] == '(':
                self._add_operation(float(value_tmp[::-1]))
            elif index+1 != len(reversed_expression) and reversed_expression[index + 1] in self._ALLOWED_OPERATIONS:
                self._add_double_operation(reversed_expression[index + 1],
                                          reversed_expression[index],
                                          float(value_tmp[::-1])
                )
            else:
                self._add_operation(float(value_tmp[::-1]), operation=reversed_expression[index])
        elif reversed_expression[index] in self._ALLOWED_SOLO_OPERATIONS:
            pass
        elif reversed_expression[index] in self._ALLOWED_OPERATIONS:
            pass

    def del_last_from_expression(self):
        self._expression = self._expression[:-1]
        self._delete_last_chosen_element()
        self._parse_backwards_and_add()

    def clear_and_get(self):
        tmp = self._expression
        self._clear_queue()
        self._expression = ''
        return tmp

    def _verify_before_calculation(self):
        if self._expression.count('(') != self._expression.count(')'):
            raise InputSyntaxError


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


calc = Calculator()



