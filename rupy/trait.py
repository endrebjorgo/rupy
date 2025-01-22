import ast
import inspect
from typing import Type
from abc import ABC, abstractmethod, ABCMeta

def trait(cls):
    for name, method in trait.__dict__.items():
        if not callable(method) or name.startswith('__'): continue

        source = inspect.getsource(method)
        tree = ast.parse(source)

        if len(tree.body) != 1 or not isinstance(tree.body[0].body[0], ast.Pass):
            raise Exception(f"Definition of trait {cls.__name__} contains erronous method")

    return ABCMeta(cls.__name__, (ABC,), dict(cls.__dict__))
