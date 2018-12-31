from ctypes import c_uint16
from enum import Enum

# https://justinmeiners.github.io/lc3-vm/

class lc3():
    def __init__(self):
        self.memory = memory()
        self.registers = registers()
        pass

'''
iirc the arch is 16bit little endian.
options: ctypes or just emulate it in pure python.
'''
class memory():
    def __init__(self):
        # ctypes has an array type. this is one way to create instances of it.
        self.memory = (c_uint16 * 65536)()

    def __getitem__(self, arg):
        if (arg > 65535) or (arg < 0):
            raise MemoryError("Accessed out valid memory range.")

        return self.memory[arg]

    def __setitem__(self, location, thing_to_write):
        if (location > 65536) or (location < 0):
            raise MemoryError("Accessed out valid memory range.")

        self.memory[location] = thing_to_write

class registers():
    def __init__():
        self.r0 = (c_uint16)()
        self.r1 = (c_uint16)()
        self.r2 = (c_uint16)()
        self.r3 = (c_uint16)()
        self.r4 = (c_uint16)()
        self.r5 = (c_uint16)()
        self.r6 = (c_uint16)()
        self.r7 = (c_uint16)()
        self.pc = (c_uint16)()
        self.cond = (c_uint16)()

# not actually a class but an enum.
class opcodes(Enum):
    op_br = 0
    op_add = 1
    op_ld = 2
    op_st = 3
    op_jsr = 4
    op_and = 5
    op_ldr = 6
    op_str = 7
    op_rti = 8
    op_not = 9
    op_ldi = 10
    op_sti = 11
    op_jmp = 12
    op_res = 13
    op_lea = 14
    op_trap = 15

class condition_flags(Enum):
    p = 0
    z = 1
    n = 2


# Load one instruction from memory at the address of the PC register.
# Increment the PC register.
# Look at the opcode to determine which type of instruction it should perform.
# Perform the instruction using the parameters in the instruction.
# Go back to step 1.


m = memory()
m[0x3000] = 4
print( m[0x3000] )

