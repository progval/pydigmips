import re
import collections

class SHIFTS:
    OPCODE = 13
    R1 = 10
    R2 = 7
    R3 = 4

INSTRUCTIONS = {}
def register(cls):
    INSTRUCTIONS[cls.opcode] = cls
    return cls

_Register = collections.namedtuple('_Register', ['id'])
class Register(_Register):
    __slots__ = ()
    @staticmethod
    def from_string(cls, s):
        if len(s) != 2 or s[0] != 'r' or s[1] not in '01234567':
            raise ValueError('%s is not a valid register name' % s)
        return Register(int(s[1]))

_ComputedAddress = collections.namedtuple('_ComputedAddress',
    ['register', 'offset'])
class ComputedAddress(_ComputedAddress):
    __slots__ = ()
    _re = re.compile('\[\s*r(?P<register>[0-7])(\s*\+\s*(?P<offset>[0-9]+))\s*\]')
    @staticmethod
    def from_string(cls, s):
        matched = cls._re.match(s)
        if not matched:
            raise ValueError('%s is not a valid computer address.' % s)
        return cls(int(matched.group('register')),
                int(matched.group('offset') or '0'))

_JumpAddress = collections.namedtuple('_JumpAddress', ['address'])
class JumpAddress(_JumpAddress):
    __slots__ = ()
    @staticmethod
    def from_string(cls, s):
        if not s.isdigit():
            raise ValueError('%s is not a valid jump address.' % s)
        return JumpAddress(int(s))

_Immediate = collections.namedtuple('_Immediate', ['value'])
class Immediate(_Immediate):
    __slots__ = ()
    @staticmethod
    def from_string(cls, s):
        if not s.isdigit():
            raise ValueError('%s is not a valid immediate.' % s)
        return Immediate(int(s))

class Instruction:
    __slots__ = ('arguments',)
    def __init__(self, *args):
        if not hasattr(self, '_spec') or not hasattr(self, '__call__') or \
                not hasattr(self, 'opcode'):
            raise NotImplementedError('%s is an abstract class.' %
                    self.__class__)
        if len(args) != len(self._spec):
            raise ValueError('%s expects %d arguments, not %d.' % (
                self.__class__.__name__.lower(),
                len(args), len(self._spec)))
        self.arguments = tuple(f(x) for (f, x) in zip(self._spec, args))

    @classmethod
    def from_bytes(cls, b):
        cls = INSTRUCTIONS[b >> SHIFTS.OPCODE]
        b %= 2**SHIFTS.OPCODE
        return cls.from_bytes(b)

    def __getitem__(self, index):
        return self.arguments[index]

    def __eq__(self, other):
        if not isinstance(other, Instruction):
            return False
        return self.opcode == other.opcode and \
                self.arguments == other.arguments



class ArithmeticInstruction(Instruction):
    __slots__ = ()
    _spec = (Register, Register, Register)

    @classmethod
    def from_bytes(cls, b):
        (r1, b) = divmod(b, 2**SHIFTS.R1)
        (r2, b) = divmod(b, 2**SHIFTS.R2)
        (r3, b) = divmod(b, 2**SHIFTS.R3)
        assert b == 0, (r1, r2, r3, b)
        return cls(r1, r2, r3)


@register
class Add(ArithmeticInstruction):
    __slots__ = ()
    opcode = 0

    def __call__(self, state):
        state.registers[self[0]] = state.registers[self[1]] + \
            state.registers[self[2]]

@register
class Sub(ArithmeticInstruction):
    __slots__ = ()
    opcode = 1

    def __call__(self, state):
        state.registers[self[0]] = state.registers[self[1]] + \
            state.registers[self[2]]

class MemoryInstruction(Instruction):
    __slots__ = ()
    _spec = (Register, ComputedAddress)

    @classmethod
    def from_bytes(cls, b):
        raise NotImplementedError() # TODO

@register
class Ld(MemoryInstruction):
    __slots__ = ()
    opcode = 2

@register
class St(MemoryInstruction):
    __slots__ = ()
    opcode = 3

@register
class Beq(Instruction):
    __slots__ = ()
    opcode = 4
    _spec = (Register, Register, JumpAddress)

    @classmethod
    def from_bytes(cls, b):
        raise NotImplementedError() # TODO

@register
class Ldi(Instruction):
    __slots__ = ()
    opcode = 5
    _spec = (Register, Immediate) # TODO: handle chars

    @classmethod
    def from_bytes(cls, b):
        raise NotImplementedError() # TODO

@register
class Ja(Instruction):
    __slots__ = ()
    opcode = 6
    _spec = (Register, Register)

    @classmethod
    def from_bytes(cls, b):
        raise NotImplementedError() # TODO

@register
class J(Instruction):
    __slots__ = ()
    opcode = 7
    _spec = (JumpAddress,)

    @classmethod
    def from_bytes(cls, b):
        raise NotImplementedError() # TODO
