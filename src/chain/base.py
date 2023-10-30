class Chain:
    def __init__(self, modules):
        self.modules = modules
    def append(self, module):
        self.modules.append(module)
    def __call__(self, input):
        pass