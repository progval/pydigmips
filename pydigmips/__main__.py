import sys
import argparse

from . import loaders
from . import emulator

def main(fd):
    program = loaders.load_hexa(fd.readlines())
    e = emulator.Emulator(program)
    try:
        e.run_all()
    except emulator.SelfLoop:
        print()
        print('Self-loop detected. (“stop: j stop”?)')
    except emulator.InfiniteLoop:
        print()
        print('Infinite loop detected (same configuration twice).')

parser = argparse.ArgumentParser(description='DigMIPS emulator.')
parser.add_argument('hexfile', metavar='hexfile',
        type=argparse.FileType('r'),
        help='The STDOUT output of the assembler')
if __name__ == '__main__':
    args = parser.parse_args()
    main(args.hexfile)
