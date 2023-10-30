from .base import Prompt

class CustomPrompt(Prompt):
    def __init__(self, template):
        self.template = template
    def __call__(self, input):
        return self.template.format(input)