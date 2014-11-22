from unittest import TestCase

from pydigmips import instructions
from pydigmips.emulator import Emulator
from pydigmips.assembly_analysis import Analyzer, Push, Pop

class AnalyzerTestCase(TestCase):
    def testPush(self):
        p = [instructions.Ldi(0, 1),
             instructions.Ldi(2, 1),
             instructions.St(4, (6, 0)),
             instructions.Sub(6, 6, 2),
             instructions.Ldi(0, 1)]
        a = Analyzer(p)
        a.analyze()
        self.assertEqual(a.pushes, {2: Push(arg=4, tmp=None)})

    def testPushReverse(self):
        p = [instructions.Ldi(0, 1),
             instructions.St(4, (6, 0)),
             instructions.Ldi(2, 1),
             instructions.Sub(6, 6, 2),
             instructions.Ldi(0, 1)]
        a = Analyzer(p)
        a.analyze()
        self.assertEqual(a.pushes, {1: Push(arg=4, tmp=None)})

    def testPop(self):
        p = [instructions.Ldi(0, 1),
             instructions.Ldi(2, 1),
             instructions.Add(6, 6, 2),
             instructions.Ld(4, (6, 0)),
             instructions.Ldi(0, 1)]
        a = Analyzer(p)
        a.analyze()
        self.assertEqual(a.pops, {3: Pop(arg=4, tmp=None)})

    def testPopReverse(self):
        p = [instructions.Ldi(0, 1),
             instructions.Add(6, 6, 2),
             instructions.Ldi(2, 1),
             instructions.Ld(4, (6, 0)),
             instructions.Ldi(0, 1)]
        a = Analyzer(p)
        a.analyze()
        self.assertEqual(a.pops, {3: Pop(arg=4, tmp=None)})

    def testStackTop(self):
        p = [instructions.Ldi(6, 255),

             instructions.Ldi(4, 42),
             instructions.Ldi(1, 1),

             instructions.Ldi(2, 1),
             instructions.St(4, (6, 0)),
             instructions.Sub(6, 6, 1),

             instructions.Ldi(5, 43),

             instructions.Ldi(2, 1),
             instructions.St(5, (6, 0)),
             instructions.Sub(6, 6, 1),

             instructions.Ldi(0, 1)]
        a = Analyzer(p)
        a.analyze()
        e = Emulator(p)
        e.run(3)
        self.assertEqual(a.get_stack_top(e.state), None)
        e.run(3)
        self.assertEqual(a.get_stack_top(e.state), 42)
        e.run(1)
        self.assertEqual(a.get_stack_top(e.state), 42)
        e.run_all()
        self.assertEqual(a.get_stack_top(e.state), 43)
