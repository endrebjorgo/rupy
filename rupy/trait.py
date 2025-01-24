import ast
import inspect
import textwrap
from typing import Type
from abc import ABC, abstractmethod, ABCMeta


def trait(cls):
    # TODO: Assert that there are only methods

    for key, value in cls.__dict__.items():
        if not callable(value) or key.startswith('__'): continue

        source = textwrap.dedent(inspect.getsource(value))
        tree = ast.parse(source)

        if len(tree.body) != 1 or not isinstance(tree.body[0].body[0], ast.Pass):
            raise Exception(f"Definition of trait {cls.__name__} contains erronous method")

    return cls

