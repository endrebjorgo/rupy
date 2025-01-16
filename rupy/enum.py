from typing import Type
from dataclasses import make_dataclass

class EnumCase:
    def __init__(self, **attributes):
        self._attributes = attributes

def enum(cls: Type) -> Type:
    """Decorator which transforms a class into a Rust-like enum."""
    for field in dir(cls):
        if not isinstance((case := getattr(cls, field)), EnumCase):
            continue

        setattr(
            cls, 
            field, 
            make_dataclass(
                field, 
                list(case._attributes.items()), 
                bases=(cls, )
            )
        )

    return cls
