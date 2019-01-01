import functools
from struct import unpack

# for now this supports programs loaded starting @ 0x3000 only

# https://stackoverflow.com/a/32031543/1234621
def sext(value, bits):
    sign_bit = 1 << (bits - 1)
    return (value & (sign_bit - 1)) - (value & sign_bit)

class UnimpError(Exception):
    pass

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

instr_lookup_table = ['BR', 'ADD', 'LD', 'ST', 'JSR', 'AND', 'LDR', 'STR', 'RTI', 'NOT', 'LDI', 'STI', 'JMP', 'RES', 'LEA', 'TRAP']

def decorator_de_decorator(func):
    pass

def extract_all_things(func):
    @functools.wraps(func) # preserve docstring, name of orig function
    def wrapper(*args, **kwargs):
        ins = args[1] # this is disgusting
        func.opcode = ins >> 12
        func.imm_bit = (ins >> 5) & 0b1
        func.jsr_bit = (ins >>11) & 0b1
        sr2 = (ins & 0b111); func.sr2 = sr2
        sr1 = (ins >> 6) & 0b111; func.sr1 = sr1
        dr = (ins >> 9) & 0b111; func.dr = dr
        imm5 = (ins & 0b11111); func.imm5 = imm5
        pc_offset_9 = sext(ins & 0x1ff, 16); func.pc_offset_9 = pc_offset_9
        func.n = 'n' if ( (ins >> 11) & 0b1 ) else ''
        func.z = 'z' if (ins >> 10) & 0b1 else ''
        func.p = 'p' if (ins >> 9) & 0b1 else ''
        pc_offset_11 = sext(ins & 0x7ff, 16); func.pc_offset_11 = pc_offset_11
        pc_offset_6 = sext(ins & 0x3f, 16); func.pc_offset_6 = pc_offset_6
        func.baser = sr1
        func.sr = sr1
        trap_vect_8 = ins & 0xff; func.trap_vect_8 = trap_vect_8

        func.__kwdefaults__ = {'self': func}
        return func(*args, **kwargs)
    return wrapper

# decorate loads function attributes with all of the possible interpretations.
@extract_all_things
def single_ins(pc, instr, *, self = 3): # asterisk: everything after this is kw only
    opcode = instr_lookup_table[self.opcode]

    if opcode == 'ADD' or opcode == 'AND':
        if not self.imm_bit:
            return '{opcode} R{dr}, R{sr1}, R{sr2}'.format(opcode=opcode, dr=self.dr, sr1=self.sr1, sr2=self.sr2)
        else: 
            return '{opcode} R{dr}, R{sr1}, #{sr2}'.format(opcode=opcode, dr=self.dr, sr1=self.sr1, sr2=self.sr2)

    if opcode == 'BR':
        return '{opcode}{n}{z}{p} {label}'.format(opcode=opcode, n=self.n, z=self.z, p=self.p, label=pc+self.pc_offset_9)

    if opcode == 'JMP':
        if self.baser == 7: # ret
            return 'RET'
        else: # jmp
            return 'JMP R{reg}'.format(reg=self.baser)

    if opcode == 'JSR':
        if self.jsr_bit:
            return 'JSR {addr}'.format(addr=pc+self.pc_offset_11)
        else:
            return 'JSRR R{reg}'.format(reg=self.baser)
            pass

    return 'not yet implemented'
    # raise UnimpError("Unimplemented")


# returns list of instructions as ints
def read_file(filename):
    li = []
    with open(filename, 'rb') as f:
        _ = f.read(2) # skip the first two byte which specify where code should be mapped
        c = f.read()  # todo support arbitrary load locations
    for count in range(0,len(c), 2):
        li.append( unpack( '>H', c[count:count+2] )[0] )
    return li


#  ADD R1, R2, #3

# if len(argv) < 2:
#     print ("usage: python3 lc3.py code.obj")
#     exit(255)

# l = read_file(argv[1])
h = read_file("second.obj")

for index,inst in enumerate(h):
    pc = index + 1 + 3000
    print( single_ins(pc, inst) )



