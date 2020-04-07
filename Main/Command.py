"""
Simple Command class that is instantiated with a name - i.e. add - prompt - "Add something" - and function - add()

Note: There is no way to add arguments to func(), because func() is usually a command line argument prompt.
"""
class Command:
    def __init__(self, name, prompt, func):
        self.name = name
        self.prompt = prompt
        self.func = func

    # Runs using given function
    def run(self):
        self.func()
