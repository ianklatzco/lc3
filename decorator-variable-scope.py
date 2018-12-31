import functools
from inspect import getmembers

# https://stackoverflow.com/a/32031543/1234621
def sext(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

# the ~~~correct~~~ way to store information for an "instruction" is probably
# a class.

# but the ~fun~ way is to use function attributes >:)
# also i want to learn more about decorators so i'm gonna abuse a bunch
# about decorators

# so, i could write a decorator for each 

# could do: a parametrized decorator on top of this that specifies which 
# field to extract, but then i can't throw it into the function attributes;
# i'd need to mix code & data somehow (or really, just use a class)

# this pains me

def decorator_de_decorator(func):
    pass

def extract_opcode(func):
    @functools.wraps(func) # preserve docstring, name of orig function
    def wrapper(*args, **kwargs):
        opcode = args[0] >> 12
        func.opcode = opcode
        func.__kwdefaults__ = {'self': func}
        return func(*args, **kwargs)
    return wrapper

def extract_dr(func):
    @functools.wraps(func) # preserve docstring, name of orig function
    def wrapper(*args, **kwargs):
        dr = (args[0] >> 9) & 0b111
        func.dr = dr
        func.__kwdefaults__ = {'self': func}
        return func(*args, **kwargs)
    return wrapper

def extract_all_things(func):
    @functools.wraps(func) # preserve docstring, name of orig function
    def wrapper(*args, **kwargs):
        ins = args[0]
        func.opcode = ins >> 12
        sr2 = (ins & 0b111); func.sr2 = sr2
        sr1 = (ins >> 6) & 0b111; func.sr1 = sr1
        dr = (ins >> 9) & 0b111; func.dr = dr
        imm5 = (ins & 0b11111); func.imm5 = imm5
        pc_offset_9 = sext(ins & 0x1ff, 16); func.pc_offset_9 = pc_offset_9
        n = (ins >> 11) & 0b1
        z = (ins >> 10) & 0b1
        p = (ins >> 9) & 0b1
        pc_offset_11 = sext(ins & 0x7ff, 16); func.pc_offset_11 = pc_offset_11
        pc_offset_6 = sext(ins & 0x3f, 16); func.pc_offset_6 = pc_offset_6
        func.baser = sr1
        func.sr = sr1
        trap_vect_8 = ins & 0xff; func.trap_vect_8 = trap_vect_8

        func.__kwdefaults__ = {'self': func}
        return func(*args, **kwargs)
    return wrapper

@extract_all_things
def ins(instr, *, self = 3): # asterisk: everything after this is kw only
    print("opcode: " + hex(self.opcode))
    print("dr:     " + hex(self.dr))
    print("sr:     " + hex(self.sr))
    print("imm5:   " + hex(self.imm5))
    pass

# ins.__kwdefaults__ = {'self': ins}
# print(getmembers(ins))

ins(0x12a3)
#  ADD R1, R2, #3

