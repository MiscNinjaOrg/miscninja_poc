from .base import Tool

class Python(Tool):
    def __init__(self):
        pass
    def run(self, input):
        return eval(input)