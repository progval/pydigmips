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

    def testJaOk(self):
        p = [instructions.Ldi(0, 0),
             instructions.Ldi(1, 5),
             instructions.Ja(0, 1)]
        e = emulator.Emulator(p)
        e.run(3)
        s = e.state
        self.assertEqual(s.pc, 5)
        self.assertRaises(emulator.Halt, e.run_one)
