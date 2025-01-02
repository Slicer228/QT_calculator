from pydantic import BaseModel, field_validator, computed_field
from typing import Any, List, Union



class OperationPageSchema(BaseModel):
    time: str
    operation: Any
    result: str

    @field_validator('result', mode='after')
    def parse_result(cls, value):
        return int(value)


class GroupOperationsSchema(BaseModel):
    pass


