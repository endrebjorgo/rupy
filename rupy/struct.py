import sys
from typing import Type
from dataclasses import dataclass

class StructImplMeta(type):
    def __new__(cls, name, bases, dct):
        module_name = dct.get('__module__')
        module_globals = sys.modules[module_name].__dict__
        if name in module_globals:
           raise Exception(f"Struct `{name}` already defined") 
        else:
            return super().__new__(cls, name, bases, dct)

class StructBase(metaclass=StructImplMeta):
    pass

def struct(cls):
    new_cls = type(cls.__name__, (StructBase, cls), dict(cls.__dict__))
    return dataclass(new_cls)
