from ctypes import c_uint16

class lc3():
    def __init__(self):
        self.memory = memory()
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



m = memory()
m[0x3000] = 4
print( m[0x3000] )