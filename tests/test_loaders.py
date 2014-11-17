from unittest import TestCase

from pydigmips import instructions, loaders

class HexaLoaderTestCase(TestCase):
    def testAdd(self):
        i = ['1510', # 000 101 010 001 0000
             '1C60',
             '2C60'] # 001 011 000 110 0000
        o = [instructions.Add(5, 2, 1), instructions.Add(7, 0, 6),
             instructions.Sub(3, 0, 6)]
        prog = loaders.load_hexa(i)
        self.assertEqual(prog, o)

    def testLd(self):
        i = ['4EAA', # 010 011 101 0101010
             '6EAA'] # 011 011 101 0101010
        o = [instructions.Ld(3, (5, 42)),
             instructions.St(3, (5, 42))]
        prog = loaders.load_hexa(i)
        self.assertEqual(prog, o)

    def testBle(self):
        i = ['8EAA'] # 100 011 101 0101010
        o = [instructions.Ble(3, 5, 42)]
        prog = loaders.load_hexa(i)
        self.assertEqual(prog, o)

    def testLdi(self):
        i = ['B0AA'] # 101 100 00 10101010
        o = [instructions.Ldi(4, 170)]
        prog = loaders.load_hexa(i)
        self.assertEqual(prog, o)
