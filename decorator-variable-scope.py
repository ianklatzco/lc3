import functools
from inspect import getmembers

# the ~~~correct~~~ way to store information for an "instruction" is probably
# a class.

# but the ~fun~ way is to use function attributes >:)

def extract_opcode(func):
    @functools.wraps(func) # preserve docstring, name of orig function
    def wrapper(*args, **kwargs):
        opcode = args[0]
        func.opcode = opcode
        func.__kwdefaults__ = {'self': func}
        return func(*args, **kwargs)
    return wrapper

@extract_opcode
def ins(instr, *, self = 3): # asterisk: everything after this is kw only
    print(hex(self.opcode))
    pass

# ins.__kwdefaults__ = {'self': ins}
# print(getmembers(ins))

ins(0x5020)
