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

