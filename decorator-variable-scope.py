import functools
from inspect import getmembers

# the ~~~correct~~~ way to store information for an "instruction" is probably
# a class.

# but the ~fun~ way is to use function attributes >:)
# also i want to learn more about decorators so i'm gonna abuse a bunch
# about decorators

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

@extract_dr
@extract_opcode
def ins(instr, *, self = 3): # asterisk: everything after this is kw only
    print("opcode: " + hex(self.opcode))
    print("dr: " + hex(self.opcode))
    pass

# ins.__kwdefaults__ = {'self': ins}
# print(getmembers(ins))

ins(0x12a3)
#  ADD R1, R2, #3

