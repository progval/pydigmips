import sys
import argparse

from . import loaders
from . import emulator
from . import compatibility

def main(fd, **kwargs):
    program = loaders.load_hexa(fd.readlines())
    e = emulator.Emulator(program, **kwargs)
    try:
        e.run_all()
    except emulator.SelfLoop:
        print()
        print('Self-loop detected. (“stop: j stop”?)')
    except emulator.InfiniteLoop:
        print()
        print('Infinite loop detected (same configuration twice).')

parser = argparse.ArgumentParser(description='DigMIPS emulator.')
parser.add_argument('hexfile',
        type=argparse.FileType('r'),
        help='The STDOUT output of the assembler')
parser.add_argument('--infinite-loop', dest='infinite_loop',
        action='store_true',
        help='Enable simple infinite loop detection (stops when '
             'the emulator has been in the same state twice.)')
parser.add_argument('--beq', dest='beq',
        action='store_true',
        help='Use old instruction set, which implements BEQ instead of '
             'BLE at opcode 4.')
parser.add_argument('--trace-inst', dest='trace_inst',
        action='store_true',
        help='Shows the Program Counter and the executed instruction '
             'while running.')
parser.add_argument('--trace-mem', dest='trace_mem',
        action='store_true',
        help='Show the state of registers and data memory while running.')
if __name__ == '__main__':
    args = parser.parse_args()
    compatibility.beq = args.beq
    main(args.hexfile, infinite_loop=args.infinite_loop,
            trace_inst=args.trace_inst, trace_mem=args.trace_mem)
