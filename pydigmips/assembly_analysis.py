"""Analyser of Assembly code that recognizes standard macros of the
compiler."""

import logging
import collections

from . import instructions

Push = collections.namedtuple('Push', ['arg', 'tmp'])
Pop = collections.namedtuple('Pop', ['arg', 'tmp'])

class Analyzer:
    def __init__(self, program):
        self.program = program

    def analyze(self):
        self.pushes = self.recognize_pushes_pops(self.recognize_push)
        self.pops = self.recognize_pushes_pops(self.recognize_pop)

    def get_stack_top(self, state):
        if state.registers[6] == 255:
            return None
        return state.data[state.registers[6]+1]

    def recognize_pushes_pops(self, f):
        instances = {}
        for i in range(0, len(self.program)-2):
            (inst1, inst2, inst3) = self.program[i:i+3]
            push = f(inst1, inst2, inst3)
            if push:
                instances[i] = push
            else:
                # The assembler does not follow the order defined in the
                # lecture.
                push = f(inst2, inst1, inst3)
                if push:
                    instances[i] = push
        return instances

    def recognize_push(self, inst1, inst2, inst3):
        try:
            (push_arg, _) = inst1.match('st', None, (6, 0))
            (push_tmp, _) = inst2.match('ldi', None, 1)
            inst3.match('sub', 6, 6, push_tmp)
            return Push(push_arg.id, push_tmp.id)
        except instructions.MatchError:
            return None

    def recognize_pop(self, inst1, inst2, inst3):
        try:
            (pop_tmp, _) = inst1.match('ldi', None, 1)
            inst2.match('add', 6, 6, pop_tmp.id)
            (pop_arg, _) = inst3.match('ld', None, (6, 0))
        except instructions.MatchError:
            return None
        return Pop(pop_arg.id, pop_tmp.id)

