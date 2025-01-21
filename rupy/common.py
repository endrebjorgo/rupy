import sys
import inspect

class ImplMeta(type):
    def __new__(cls, name, bases, dct):
        module_name = dct.get('__module__')
        module_globals = sys.modules[module_name].__dict__
        if name in module_globals:
            print(f"Class {name} already exists.")
        return super().__new__(cls, name, bases, dct)

def unreachable():
    raise Exception("internal error: entered unreachable code")
