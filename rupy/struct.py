import sys
from typing import Callable, Type
from dataclasses import dataclass

class StructImplMeta(type):
    def __new__(cls, name, bases, dct):
        module_name = dct.get('__module__')
        module_globals = sys.modules[module_name].__dict__
        if name in module_globals:
            if annotations := dct.get("__annotations__"):
                new_annotations = [x for x in annotations]
                if new_annotations:
                    raise Exception(f"Cannot add struct fields more than once: {new_annotations}")

            existing_cls = module_globals[name]
            for key, value in dct.items():
                if key not in ('__module__', '__qualname__', '__dict__'):
                    setattr(existing_cls, key, value)
            return existing_cls
        else:
            return super().__new__(cls, name, bases, dct)

class StructBase(metaclass=StructImplMeta):
    pass

def struct(cls):
    new_cls = type(cls.__name__, (StructBase, cls), dict(cls.__dict__))
    return dataclass(new_cls)

