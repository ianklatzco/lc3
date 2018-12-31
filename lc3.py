from ctypes import c_uint16, c_int16
from enum import IntEnum
from binascii import *
from struct import unpack
from sys import exit

# https://justinmeiners.github.io/lc3-vm/

# Load one instruction from memory at the address of the PC register.
# Increment the PC register.
# Look at the opcode to determine which type of instruction it should perform.
# Perform the instruction using the parameters in the instruction.
# Go back to step 1.

DEBUG = False

# https://stackoverflow.com/a/32031543/1234621
def sext(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

class lc3():
    def __init__(self, filename):
        self.memory = memory()
        self.registers = registers()
        self.registers.pc.value = 0x3000 # default program starting location
        self.read_program_from_file(filename)

    def read_program_from_file(self,filename):
        with open(filename, 'rb') as f:
            _ = f.read(2) # skip the first two byte which specify where code should be mapped
            c = f.read()  # todo support arbitrary load locations
        for count in range(0,len(c), 2):
            self.memory[0x3000+count/2] = unpack( '>H', c[count:count+2] )[0]

    def update_flags(self, reg):
        if self.registers.gprs[reg] == 0:
            self.registers.cond = condition_flags.z
        if self.registers.gprs[reg] < 0:
            self.registers.cond = condition_flags.n
        if self.registers.gprs[reg] > 0:
            self.registers.cond = condition_flags.p

    def dump_state(self):
        print("pc: {:04x}".format(self.registers.pc.value))
        print("r0: {:05} ".format(self.registers.gprs[0]), end='')
        print("r1: {:05} ".format(self.registers.gprs[1]), end='')
        print("r2: {:05} ".format(self.registers.gprs[2]), end='')
        print("r3: {:05} ".format(self.registers.gprs[3]), end='')
        print("r4: {:05} ".format(self.registers.gprs[4]), end='')
        print("r5: {:05} ".format(self.registers.gprs[5]), end='')
        print("r6: {:05} ".format(self.registers.gprs[6]), end='')
        print("r7: {:05} ".format(self.registers.gprs[7]))

        print("r0:  {:04x} ".format(c_uint16(self.registers.gprs[0]).value), end='')
        print("r1:  {:04x} ".format(c_uint16(self.registers.gprs[1]).value), end='')
        print("r2:  {:04x} ".format(c_uint16(self.registers.gprs[2]).value), end='')
        print("r3:  {:04x} ".format(c_uint16(self.registers.gprs[3]).value), end='')
        print("r4:  {:04x} ".format(c_uint16(self.registers.gprs[4]).value), end='')
        print("r5:  {:04x} ".format(c_uint16(self.registers.gprs[5]).value), end='')
        print("r6:  {:04x} ".format(c_uint16(self.registers.gprs[6]).value), end='')
        print("r7:  {:04x} ".format(c_uint16(self.registers.gprs[7]).value))

        print("cond: {}".format(condition_flags(self.registers.cond.value).name))

    def op_add_impl(self, instruction):
        sr1 = (instruction >> 6) & 0b111
        dr  = (instruction >> 9) & 0b111
        if ((instruction >> 5) & 0b1) == 0: # reg-reg
            sr2 = instruction & 0b111
            self.registers.gprs[dr] = self.registers.gprs[sr1] + self.registers.gprs[sr2]
        else: # immediate
            imm5 = instruction & 0b11111 
            self.registers.gprs[dr] = self.registers.gprs[sr1] + sext(imm5, 5)
        self.update_flags(dr)

    def op_and_impl(self, instruction):
        sr1 = (instruction >> 6) & 0b111
        dr  = (instruction >> 9) & 0b111

        if ((instruction >> 5) & 0b1) == 0: # reg-reg
            sr2 = instruction & 0b111
            self.registers.gprs[dr] = self.registers.gprs[sr1] & self.registers.gprs[sr2]
        else: # immediate
            imm5 = instruction & 0b11111 
            self.registers.gprs[dr] = self.registers.gprs[sr1] & sext(imm5, 5)

        self.update_flags(dr)

    def op_not_impl(self, instruction):
        sr  = (instruction >> 6) & 0b111
        dr  = (instruction >> 9) & 0b111

        self.registers.gprs[dr] = ~ (self.registers.gprs[sr])

        self.update_flags(dr)

    def op_br_impl(self, instruction):
        n = (instruction >> 11) & 1
        z = (instruction >> 10) & 1
        p = (instruction >> 9) & 1
        pc_offset_9 = instruction & 0x1ff

        if  (n == 1 and self.registers.cond == condition_flags.n) or \
            (z == 1 and self.registers.cond == condition_flags.z) or \
            (p == 1 and self.registers.cond == condition_flags.p):
            self.registers.pc.value = self.registers.pc.value + sext(pc_offset_9, 9)

    # also ret
    def op_jmp_impl(self, instruction):
        baser = (instruction >> 6) & 0b111

        self.registers.pc.value = self.registers.gprs[baser]

    def op_jsr_impl(self, instruction):
        # no jsrr?
        pc_offset_11 = instruction & 0x7ff

        self.registers.gprs[7] = self.registers.pc.value
        self.registers.pc.value = self.registers.pc.value + sext(pc_offset_11, 11)

    def op_ld_impl(self, instruction):
        dr = (instruction >> 9) & 0b111
        pc_offset_9 = instruction & 0x1ff
        addr = self.registers.pc.value + sext(pc_offset_9, 9)
        self.registers.gprs[dr] = self.memory[addr]
        self.update_flags(dr)

    def op_ldi_impl(self, instruction):
        dr = (instruction >> 9) & 0b111
        pc_offset_9 = instruction & 0x1ff
        addr = self.registers.pc.value + sext(pc_offset_9, 9)
        self.registers.gprs[dr] = self.memory[ self.memory[addr] ]
        self.update_flags(dr)

    def op_ldr_impl(self, instruction):
        raise Error("unimplemented opcode")

    def op_lea_impl(self, instruction):
        dr = (instruction >> 9) & 0b111
        pc_offset_9 = instruction & 0x1ff

        self.registers.gprs[dr] = self.registers.pc.value + sext(pc_offset_9, 9)
        self.update_flags(dr)

    def op_st_impl(self, instruction):
        raise Error("unimplemented opcode")
    def op_sti_impl(self, instruction):
        raise Error("unimplemented opcode")
    def op_str_impl(self, instruction):
        raise Error("unimplemented opcode")
    def op_trap_impl(self, instruction):
        # todo: implement more than just halt
        self.dump_state()
        exit()
    def op_res_impl(self, instruction):
        raise Error("unimplemented opcode")
    def op_rti_impl(self, instruction):
        raise Error("unimplemented opcode")

    def start(self):
        while True:
            # fetch instruction
            instruction = self.memory[self.registers.pc.value]

            # update PC
            self.registers.pc.value = self.registers.pc.value + 1

            # decode opcode
            opcode = instruction >> 12

            # if debug = true
            if DEBUG:
                print(opcodes(opcode))
                self.dump_state()
                input()

            # decoding of the instruction should happen here
            if opcode == opcodes.op_add:
                self.op_add_impl(instruction)
            elif opcode == opcodes.op_and:
                self.op_and_impl(instruction)
            elif opcode == opcodes.op_not:
                self.op_not_impl(instruction)
            elif opcode == opcodes.op_br:
                self.op_br_impl(instruction)
            elif opcode == opcodes.op_jmp:
                self.op_jmp_impl(instruction)
            elif opcode == opcodes.op_jsr:
                self.op_jsr_impl(instruction)
            elif opcode == opcodes.op_ld:
                self.op_ld_impl(instruction)
            elif opcode == opcodes.op_ldi:
                self.op_ldi_impl(instruction)
            elif opcode == opcodes.op_ldr:
                self.op_ldr_impl(instruction)
            elif opcode == opcodes.op_lea:
                self.op_lea_impl(instruction)
            elif opcode == opcodes.op_st:
                self.op_st_impl(instruction)
            elif opcode == opcodes.op_sti:
                self.op_sti_impl(instruction)
            elif opcode == opcodes.op_str:
                self.op_str_impl(instruction)
            elif opcode == opcodes.op_trap:
                self.op_trap_impl(instruction)
            elif opcode == opcodes.op_res:
                self.op_res_impl(instruction)
            elif opcode == opcodes.op_rti:
                self.op_rti_impl(instruction)
            else:
                raise Error("invalid opcode")


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

        self.memory[int(location)] = thing_to_write

class registers():
    def __init__(self):
        self.gprs = (c_int16 * 8)()
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
