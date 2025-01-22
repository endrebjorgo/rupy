from typing import Type, Callable

from .struct import struct

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
