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
    value: float | int


class GroupOperationSchema(BaseModel):
    operation: Any
    group: List


class ExpressionSchema(BaseModel):
    current_result: float | int | None
    prev_result: float | int | None
    prev_expression: GroupOperationSchema
    current_expression: GroupOperationSchema




