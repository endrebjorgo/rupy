from dataclasses import make_dataclass
from typing import TypeVar, Generic, Type, Callable

T = TypeVar("T")

def enum(cls: Type) -> Type:
    for field_name in dir(cls):
        if not isinstance((value := getattr(cls, field_name)), Case): continue
        setattr(cls, field_name, make_dataclass(field_name, list(value._attributes.items()), bases=(cls, )))
    return cls

class Case:
    def __init__(self, **attributes):
        self._attributes = attributes

@enum
class Option[T]:
    Some = Case(value=T)
    Not = Case()

    def unwrap(self) -> T:
        match self:
            case Option.Some(value): return value
            case _: raise Exception

    def unwrap_or(self, default: T) -> T:
        match self:
            case Option.Some(value): return value
            case _: return default 

    def unwrap_or_else(self, f: Callable[[...], T]) -> T:
        match self:
            case Option.Some(value): return value
            case _: return f() 


    """
    def unwrap_or_default(self) -> T:
        match self:
            case Option.Some(value): return value
            case _: return type(T)()
    """

def option_convert(f: Callable[[...], T]) -> Callable[[...], Option[T]]:
    def wrapper(*args, **kwargs) -> Option[T]:
        result = f(*args, **kwargs)
        if result is None:
            return Option.Not()
        else:
            return Option.Some(result)

    return wrapper

@enum
class Result[T]:
    Ok = Case(value=T)
    Err = Case(msg=str)

@option_convert
def none_if_odd(n: int):
    if n % 2 == 1:
        return None
    else:
        return 1

if __name__ == "__main__":
    """
    x: Option[int] = Option.Not()
    print(x)
    y = x.unwrap_or_default()
    print(y)
    """
    a = none_if_odd(1)
    print(a)

