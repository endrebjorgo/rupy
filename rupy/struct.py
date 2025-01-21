import sys
from typing import Type
from dataclasses import make_dataclass, dataclass

from .common import ImplMeta

class StructBase(metaclass=ImplMeta):
    pass

def struct(cls):
    new_cls = type(cls.__name__, (StructBase, cls), dict(cls.__dict__))
    return dataclass(new_cls)
