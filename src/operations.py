from enum import Enum


def add(a, b):
    return a + b


def divide(a, b):
    return a / b


def subtract(a, b):
    return a - b


def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


class Operations(Enum):
    ADD = add
    DIVIDE = divide
    SUBTRACT = subtract


class SoloOperations(Enum):
    FACTORIAL = factorial
