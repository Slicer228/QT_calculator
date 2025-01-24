from src.core.query import CalculatorQueryHandler
from src.exceptions import InputSyntaxError


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