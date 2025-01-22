from typing import Type, Callable

"""
def impl(trait: Type) -> Callable[[Type], Type]:
    def decorator(cls):
        new_cls = type(
            cls.__name__,
            (trait, cls),
            dict(cls.__dict__)
        )
        return new_cls 
    return decorator
"""
