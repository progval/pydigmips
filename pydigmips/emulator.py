from .state import State

class Halt(Exception):
    pass

class Emulator:
    def __init__(self, program, state=None, beq=False):
        self.program = program
        self.state = state or State()

    def run_one(self):
        if self.state.pc >= len(self.program):
            raise Halt()
        inst = self.program[self.state.pc]
        inst(self.state)
        self.state.pc += 1

    def run(self, max_steps):
        for x in range(0, max_steps):
            self.run_one()
