# https://realpython.com/primer-on-python-decorators/#simple-decorators
import functools

def dec(func):
    @functools.wraps(func) # preserve docstring, name of orig function
    def wrapper(*args, **kwargs):
        print("pre")
        return func(*args, **kwargs)
    return wrapper

@dec
def foo(instr):
    print("bar")

foo(0x5020)
