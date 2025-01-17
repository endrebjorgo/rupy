from abc import ABC, abstractmethod
from typing import Type

def trait(cls: Type) -> Type:
    methods = {
        func: abstractmethod(getattr(cls, func)) 
        for func in dir(cls) 
        if callable(getattr(cls, func)) and not func.startswith("__")
    }
    return type(cls.__name__, (ABC,), methods)
