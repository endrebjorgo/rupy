import sys
from typing import Callable, Type
from dataclasses import dataclass
from abc import ABCMeta

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

class StructBaseMeta(StructImplMeta, ABCMeta):
    pass

class StructBase(metaclass=StructBaseMeta):
    pass

def struct(cls):
    new_cls = type(cls.__name__, (StructBase, cls), dict(cls.__dict__))
    return dataclass(new_cls)

def impl(trait: Type) -> Callable[[Type], Type]:
    def decorator(cls):
        # TODO: Replace the following with ABC functionality
        a = [
            key for key, val in trait.__dict__.items() 
            if callable(val) and not key.startswith('__')
        ]
        b = [
            key for key, val in cls.__dict__.items() 
            if callable(val) and not key.startswith('__')
        ]
        if set(a) != set(b):
            raise Exception(f"Implementation of trait `{trait.__name__}` for `{cls.__name__}` does not contain correct methods")

        new_cls = type(
            cls.__name__,
            (trait, cls),
            dict(cls.__dict__)
        )
        return struct(new_cls)

    return decorator


