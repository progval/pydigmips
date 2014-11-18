import sys
import io
from unittest import TestCase

from pydigmips import instructions, state, emulator

class EmulatorTestCase(TestCase):
    def testRun(self):
        p = [instructions.Ldi(0, 42),
             instructions.Ldi(1, 5)]
        e = emulator.Emulator(p)
        e.run_one()
        s = e.state
        self.assertEqual(s.registers[0], 42)
        self.assertEqual(s.registers[1], 0)
        e.run_one()
        self.assertEqual(s.registers[0], 42)
        self.assertEqual(s.registers[1], 5)

    def testHalt(self):
        p = [instructions.Ldi(0, 42),
             instructions.Ldi(1, 5)]
        e = emulator.Emulator(p)
        e.run_one()
        e.run_one()
        self.assertRaises(emulator.Halt, e.run_one)

    def testAdd(self):
        p = [instructions.Ldi(0, 42),
             instructions.Ldi(1, 5),
             instructions.Add(2, 0, 1)]
        e = emulator.Emulator(p)
        e.run(3)
        s = e.state
        self.assertEqual(s.registers[0], 42)
        self.assertEqual(s.registers[1], 5)
        self.assertEqual(s.registers[2], 47)

    def testSub(self):
        p = [instructions.Ldi(1, 1),
             instructions.Ldi(2, 2),
             instructions.Sub(3, 1, 2),
             instructions.Ldi(2, ord('N')),
             instructions.Add(3, 3, 2),
             instructions.St(3, (4, 63))]
        e = emulator.Emulator(p)
        (original_stdout, sys.stdout) = (sys.stdout, io.StringIO())
        try:
            e.run(6)
        finally:
            (sys.stdout, stream) = (original_stdout, sys.stdout)
        stream.seek(0)
        self.assertEqual(stream.read(), 'M')

    def testBleFalse(self):
        p = [instructions.Ldi(0, 42),
             instructions.Ldi(1, 5),
             instructions.Ble(0, 1, 1),
             instructions.Ldi(2, 42),
             instructions.Ldi(3, 42)]
        e = emulator.Emulator(p)
        e.run(4)
        s = e.state
        self.assertEqual(s.pc, 4)
        self.assertEqual(s.registers[2], 42)
        self.assertEqual(s.registers[3], 0)
        e.run(1)
        self.assertEqual(s.pc, 5)
        self.assertEqual(s.registers[2], 42)
        self.assertEqual(s.registers[3], 42)
        self.assertRaises(emulator.Halt, e.run_one)

    def testBleTrue(self):
        p = [instructions.Ldi(0, 42),
             instructions.Ldi(1, 43),
             instructions.Ble(0, 1, 1),
             instructions.Ldi(2, 42),
             instructions.Ldi(3, 42)]
        e = emulator.Emulator(p)
        e.run(4)
        s = e.state
        self.assertEqual(s.pc, 5)
        self.assertEqual(s.registers[2], 0)
        self.assertEqual(s.registers[3], 42)
        self.assertRaises(emulator.Halt, e.run_one)

    def testSt(self):
        p = [instructions.Ldi(0, 5),
             instructions.Ldi(1, 42),
             instructions.St(1, (0, 10))]
        e = emulator.Emulator(p)
        e.run(3)
        s = e.state
        self.assertEqual(s.data[15], 42, s.data)

    def testLd(self):
        p = [instructions.Ldi(0, 5),
             instructions.Ldi(1, 42),
             instructions.St(1, (0, 10)),
             instructions.Ld(2, (0, 10))]
        e = emulator.Emulator(p)
        e.run(4)
        s = e.state
        self.assertEqual(s.registers[2], 42)


    def testJaSmall(self):
        p = [instructions.Ldi(0, 0),
             instructions.Ldi(1, 5),
             instructions.Ja(0, 1)]
        e = emulator.Emulator(p)
        e.run(3)
        s = e.state
        self.assertEqual(s.pc, 5)
        self.assertRaises(emulator.Halt, e.run_one)

    def testJaBig(self):
        p = [instructions.Ldi(0, 1),
             instructions.Ldi(1, 5),
             instructions.Ja(0, 1)]
        e = emulator.Emulator(p)
        e.run(3)
        s = e.state
        self.assertEqual(s.pc, 2**8 + 5)
        self.assertRaises(emulator.Halt, e.run_one)

    def testJ(self):
        p = [instructions.J(5)]
        e = emulator.Emulator(p)
        e.run(1)
        s = e.state
        self.assertEqual(s.pc, 5)
        self.assertRaises(emulator.Halt, e.run_one)

    def testOutput(self):
        p = [instructions.Ldi(0, ord('P')),
             instructions.Ldi(1, ord('Y')),
             instructions.St(0, (7, 63)),
             instructions.St(1, (7, 63))]
        e = emulator.Emulator(p)
        (original_stdout, sys.stdout) = (sys.stdout, io.StringIO())
        try:
            e.run(4)
        finally:
            (sys.stdout, stream) = (original_stdout, sys.stdout)
        stream.seek(0)
        self.assertEqual(stream.read(), 'PY')

    def testInput(self):
        p = [instructions.Ld(0, (7, 63)),
             instructions.Ld(1, (7, 63))]
        e = emulator.Emulator(p)
        stream = io.StringIO('PY')
        stream.seek(0)
        (original_stdin, sys.stdin) = (sys.stdin, stream)
        try:
            e.run(2)
        finally:
            (sys.stdin, stream) = (original_stdin, sys.stdin)
        s = e.state
        self.assertEqual(s.registers[0], ord('P'))
        self.assertEqual(s.registers[1], ord('Y'))

    def testInfiniteLoop(self):
        p = [instructions.Ldi(0, 42),
             instructions.J(0)]
        e = emulator.Emulator(p, infinite_loop=True)
        e.run(1) # LDI
        e.run(1) # J
        self.assertRaises(emulator.InfiniteLoop, e.run, 1) # LDI

    def testSelfLoop(self):
        p = [instructions.Ldi(0, 42),
             instructions.J(1)]
        e = emulator.Emulator(p)
        e.run(1)
        self.assertRaises(emulator.SelfLoop, e.run, 1)
