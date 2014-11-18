import sys
import argparse

from . import loaders
from . import emulator

def main(fd, **kwargs):
    program = loaders.load_hexa(fd.readlines())
    e = emulator.Emulator(program, **kwargs)
    try:
        e.run_all()
    except emulator.SelfLoop:
        print()
        print('Self-loop detected. (“stop: j stop”?)')
        print('{0} instructions were executed.'.format(str(e.state.numberInstructions)))
    except emulator.InfiniteLoop:
        print()
        print('Infinite loop detected (same configuration twice).')
        print('{0} instructions were executed.'.format(str(e.state.numberInstructions)))

parser = argparse.ArgumentParser(description='DigMIPS emulator.')
parser.add_argument('hexfile',
        type=argparse.FileType('r'),
        help='The STDOUT output of the assembler')
parser.add_argument('--infinite-loop', dest='infinite_loop',
        action='store_true')
parser.add_argument('--beq', dest='beq',
        action='store_true')
parser.add_argument('--trace-inst', dest='trace_inst',
        action='store_true')
parser.add_argument('--trace-mem', dest='trace_mem',
        action='store_true')
if __name__ == '__main__':
    args = parser.parse_args()
    main(args.hexfile, infinite_loop=args.infinite_loop, beq=args.beq,
            trace_inst=args.trace_inst, trace_mem=args.trace_mem)
