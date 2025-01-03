from src.operations import Operations, SoloOperations


sheet = {
    '+': Operations.ADD.value,
    '-': Operations.SUBTRACT.value,
    '!': SoloOperations.FACTORIAL.value,
    '/': Operations.DIVIDE.value,
    '*': Operations.MULTIPLY.value,
    None: None
}
