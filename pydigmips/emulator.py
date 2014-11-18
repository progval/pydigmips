import time

from .state import State

DETECT_SAME_CONFIG = True

class Halt(Exception):
    pass
class InfiniteLoop(Exception):
    pass
class SelfLoop(Exception):
    """Raised when an instruction jumps to itself."""

class Emulator:
    def __init__(self, program, state=None, beq=False):
        self.program = program
        self.state = state or State()
        self.previous_states = set()

    def run_one(self):
        if self.state.pc >= len(self.program):
            raise Halt()
        inst = self.program[self.state.pc]
        old_pc = self.state.pc
        self.state.pc += 1
        inst(self.state)
        if self.state.pc == old_pc:
            raise SelfLoop()
        if DETECT_SAME_CONFIG:
            if self.state.freeze() in self.previous_states:
                raise InfiniteLoop()
            self.previous_states.add(self.state.freeze())

    def run(self, max_steps):
        for x in range(0, max_steps):
            self.run_one()

    def run_all(self):
        try:
            while True:
                self.run_one()
        except Halt:
            pass
