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
        if not isinstance(inst1, instructions.St) or \
                inst1[1].register != 6 or \
                inst1[1].offset != 0:
            return 
        push_arg = inst1[0].id
        if not isinstance(inst2, instructions.Ldi) or \
                inst2[1].value != 1:
            return 
        push_tmp = inst2[0].id
        if inst3 != instructions.Sub(6, 6, push_tmp):
            return
        return Push(push_arg, push_tmp)

    def recognize_pop(self, inst1, inst2, inst3):
        if not isinstance(inst1, instructions.Ldi) or \
                inst1[1].value != 1:
            return 
        pop_tmp = inst1[0].id
        if inst2 != instructions.Add(6, 6, pop_tmp):
            return
        if not isinstance(inst3, instructions.Ld) or \
                inst3[1].register != 6 or \
                inst3[1].offset != 0:
            return
        pop_arg = inst3[0].id
        return Pop(pop_arg, pop_tmp)

