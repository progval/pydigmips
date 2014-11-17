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

