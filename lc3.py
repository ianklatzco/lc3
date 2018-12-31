from ctypes import c_uint16
from enum import IntEnum
from binascii import *
from struct import unpack

# https://justinmeiners.github.io/lc3-vm/

# Load one instruction from memory at the address of the PC register.
# Increment the PC register.
# Look at the opcode to determine which type of instruction it should perform.
# Perform the instruction using the parameters in the instruction.
# Go back to step 1.

class lc3():
    def __init__(self, filename):
        self.memory = memory()
        self.registers = registers()
        self.registers.pc.value = 0x3000 # default program starting location
        self.read_program_from_file(filename)

    def read_program_from_file(self,filename):
        with open(filename, 'rb') as f:
            _ = f.read(2) # skip the first two byte which specify where code should be mapped
            c = f.read()
        for count in range(0,len(c), 2):
            self.memory[0x3000+count/2] = unpack( '>H', c[count:count+2] )[0]

    def op_add_impl(self):
        raise Error("unimplemented opcode")
    def op_and_impl(self):
        raise Error("unimplemented opcode")
    def op_not_impl(self):
        raise Error("unimplemented opcode")
    def op_br_impl(self):
        raise Error("unimplemented opcode")
    def op_jmp_impl(self):
        raise Error("unimplemented opcode")
    def op_jsr_impl(self):
        raise Error("unimplemented opcode")
    def op_ld_impl(self):
        raise Error("unimplemented opcode")
    def op_ldr_impl(self):
        raise Error("unimplemented opcode")
    def op_lea_impl(self):
        raise Error("unimplemented opcode")
    def op_st_impl(self):
        raise Error("unimplemented opcode")
    def op_sti_impl(self):
        raise Error("unimplemented opcode")
    def op_str_impl(self):
        raise Error("unimplemented opcode")
    def op_trap_impl(self):
        raise Error("unimplemented opcode")
    def op_res_impl(self):
        raise Error("unimplemented opcode")
    def op_rti_impl(self):
        raise Error("unimplemented opcode")

    def start(self):
        running = 1
        while running < 10:
            # fetch instruction
            fetched_instruction = self.memory[self.registers.pc.value]

            # update PC
            self.registers.pc.value = self.registers.pc.value + 1

            # decode opcode
            opcode = fetched_instruction >> 12

            if opcode == opcodes.op_add:
                self.op_add_impl()
            elif opcode == opcodes.op_and:
                self.op_and_impl()
            elif opcode == opcodes.op_not:
                self.op_not_impl()
            elif opcode == opcodes.op_br:
                self.op_br_impl()
            elif opcode == opcodes.op_jmp:
                self.op_jmp_impl()
            elif opcode == opcodes.op_jsr:
                self.op_jsr_impl()
            elif opcode == opcodes.op_ld:
                self.op_ld_impl()
            elif opcode == opcodes.op_ldr:
                self.op_ldr_impl()
            elif opcode == opcodes.op_lea:
                self.op_lea_impl()
            elif opcode == opcodes.op_st:
                self.op_st_impl()
            elif opcode == opcodes.op_sti:
                self.op_sti_impl()
            elif opcode == opcodes.op_str:
                self.op_str_impl()
            elif opcode == opcodes.op_trap:
                self.op_trap_impl()
            elif opcode == opcodes.op_res:
                self.op_res_impl()
            elif opcode == opcodes.op_rti:
                self.op_rti_impl()
            else:
                raise Error("invalid opcode")

            running = running + 1


'''
iirc the arch is 16bit little endian.
options: ctypes or just emulate it in pure python.
chose: ctypes
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
    def __init__(self):
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
class opcodes(IntEnum):
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

class condition_flags(IntEnum):
    p = 0
    z = 1
    n = 2


l = lc3("second.obj")
l.start()