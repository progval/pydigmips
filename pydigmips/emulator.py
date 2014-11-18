import time

from .state import State

class Halt(Exception):
    pass
class InfiniteLoop(Exception):
    pass
class SelfLoop(Exception):
    """Raised when an instruction jumps to itself."""

class Emulator:
    def __init__(self, program, state=None, beq=False, infinite_loop=False,
            trace_inst=False, trace_mem=False):
        self.trace_inst = trace_inst
        self.trace_mem = trace_mem
        self.program = program
        self.state = state or State()
        self.previous_states = set()
        self.detect_same_config = infinite_loop

    def run_one(self):
        if self.state.pc >= len(self.program):
            raise Halt()
        inst = self.program[self.state.pc]
        if self.trace_mem:
            print('Registers: %r' % self.state.registers)
            print('Data: %r' % (self.state.data))
        if self.trace_inst:
            print('%.03d: %s' % (self.state.pc, inst))
        old_pc = self.state.pc
        self.state.pc += 1
        self.state.numberInstructions += 1
        inst(self.state)
        if self.state.pc == old_pc:
            raise SelfLoop()
        if self.detect_same_config:
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
