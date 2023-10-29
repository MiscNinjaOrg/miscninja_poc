from .base import Tool

class Calculator(Tool):
    def __init__(self):
        pass
    def run(self, input):
        return eval(input)