from enum import Enum
from src.schemas import InternalOperationSchema


def add(a, b):
    return a + b


def divide(a, b):
    return a / b


def subtract(a, b):
    return a - b


def factorial(n):
    f = 1
    for i in range(1,int(n)+1):
        f *= i
    return f


def multiply(a, b):
    return a * b


def foo():
    pass


class Operations(Enum):
    MULTIPLY = InternalOperationSchema(executable=multiply, priority=3, perfomance='*')
    ADD = InternalOperationSchema(executable=add, priority=4, perfomance='+')
    DIVIDE = InternalOperationSchema(executable=divide, priority=2, perfomance='/')
    SUBTRACT = InternalOperationSchema(executable=subtract, priority=5, perfomance='-')


class SoloOperations(Enum):
    FACTORIAL = InternalOperationSchema(executable=factorial, priority=1, perfomance='!')
    NO_OPERATION = InternalOperationSchema(executable=foo, priority=0, perfomance='')
