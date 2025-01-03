from src.convert_input import sheet
from src.schemas import OperationSchema, GroupOperationSchema
from src.exceptions import InputSyntaxError


class Calculator:
    ALLOWED_FIRST_OPERATIONS = '!'
    queue = []
    groups_deep_len = 0
    current_group = queue

    def add_group_to_queue(self, operation = None):
        if len(self.current_group) == 0 and operation not in self.ALLOWED_FIRST_OPERATIONS:
            raise InputSyntaxError
        if len(self.current_group) > 0 and operation in self.ALLOWED_FIRST_OPERATIONS:
            raise InputSyntaxError
        self.current_group.append(GroupOperationSchema(
            operation=sheet[operation],
            group=[]
        ))
        self.groups_deep_len += 1
        self.current_group = self.current_group[-1].group

    def end_group(self):
        self.groups_deep_len = self.groups_deep_len - 1 if self.groups_deep_len >= 1 else 0
        self.go_to_current_new_group()

    def add_operation(self, value, operation = None):
        if len(self.current_group) == 0 and operation not in self.ALLOWED_FIRST_OPERATIONS:
            raise InputSyntaxError
        if len(self.current_group) > 0 and operation in self.ALLOWED_FIRST_OPERATIONS:
            raise InputSyntaxError
        self.current_group.append(OperationSchema(
            operation=sheet[operation],
            value=value
        ))

    def add_double_operation_group(self,operation,solo_operation):
        if len(self.current_group) == 0:
            raise InputSyntaxError
        self.current_group.append(GroupOperationSchema(
            operation=(sheet[operation], sheet[solo_operation]),
            group=[]
        ))
        self.groups_deep_len += 1
        self.current_group = self.current_group[-1].group

    def add_double_operation(self,operation,solo_operation,value):
        if len(self.current_group) == 0:
            raise InputSyntaxError
        self.current_group.append(OperationSchema(
            operation=(sheet[operation], sheet[solo_operation]),
            value=value
        ))

    def delete_last_chosen_element(self):
        if self.queue:
            if len(self.current_group) == 0:
                self.groups_deep_len -= 1
                self.go_to_current_new_group()
                self.current_group.pop()
            else:
                self.current_group.pop()

    def go_to_current_new_group(self):
        if self.queue:
            self.current_group = self.queue[-1].group if self.groups_deep_len else self.queue
            for i in range(self.groups_deep_len - 1):
                self.current_group = self.current_group[-1].group

    def print_group(self,group):
        print('(',end='')
        for i in group:
            if isinstance(i,OperationSchema):
                print(i.operation.perfomance if not(isinstance(i.operation,tuple)) else i.operation[0].perfomance + ' ' + i.operation[1].perfomance,i.value,end=' ',sep='')
            else:
                print(i.operation.perfomance if not(isinstance(i.operation,tuple)) else i.operation[0].perfomance + ' ' + i.operation[1].perfomance,end='')
                self.print_group(i.group)
        print(')', end='')

    def print_queue(self):
        self.print_group(self.queue)


calc = Calculator()


