from pydantic import BaseModel, field_validator
from typing import Any, Callable, List, Union, Self, Optional, Tuple


class OperationPageSchema(BaseModel):
    time: str
    operation: Any
    result: str

    @field_validator('result', mode='after')
    def parse_result(cls, value):
        return int(value)


class InternalOperationSchema(BaseModel):
    perfomance: str
    executable: Callable
    priority: int


class OperationSchema(BaseModel):
    operation: Any

    def __eq__(self, current_priority):
        if isinstance(self.operation, tuple) and self.operation[0].priority == current_priority:
            return True
        elif isinstance(self.operation, InternalOperationSchema) and self.operation.priority == current_priority:
            return True
        else:
            return False


class SingleOperationSchema(OperationSchema):
    value: float | int


class GroupOperationSchema(OperationSchema):
    group: List
    _i = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self._i < len(self.group):
            self._i += 1
            return self.group[self._i-1]
        self._i = 0
        raise StopIteration

    def __len__(self):
        return len(self.group)

    def __getitem__(self, item):
        return self.group[item]

    def pop(self, index):
        self.group.pop(index)

class ExpressionSchema(BaseModel):
    current_result: float | int | None
    prev_result: float | int | None
    prev_expression: GroupOperationSchema
    current_expression: GroupOperationSchema




