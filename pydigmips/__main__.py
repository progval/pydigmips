import sys

from . import loaders
from . import emulator

def main(filename):
    with open(filename) as fd:
        program = loaders.load_hexa(fd.readlines())
    e = emulator.Emulator(program)
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

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Syntax: %s file.ram' % sys.argv[0])
        exit(1)
    main(sys.argv[1])
