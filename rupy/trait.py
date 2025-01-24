import ast
import inspect
import textwrap
from typing import Type
from abc import ABC, abstractmethod, ABCMeta


def trait(cls):
    for key, value in cls.__dict__.items():
        if key.startswith('__'): continue
        if not callable(value):
            raise Exception(f"Trait definition may not contain attributes: {cls.__name__}")

        source = textwrap.dedent(inspect.getsource(value))
        tree = ast.parse(source)

        if len(tree.body) != 1 or not isinstance(tree.body[0].body[0], ast.Pass):
            raise Exception(f"Trait method definition may only contain pass: {cls.__name__}")

    return cls

