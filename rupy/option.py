from typing import TypeVar, Callable

from .enum import enum, EnumCase
from .common import unreachable
#from .result import Result

T = TypeVar("T")
E = TypeVar("E")

@enum
class Option[T]:
    Some = EnumCase(value=T)
    Not = EnumCase()

    """
    def ok_or(self, err: E) -> Result[T, E]:
        match self:
            case Option.Some(value): return Result.Ok(value)
            case Option.Not(): return Result.Err(err)
    """

    def unwrap(self) -> T:
        match self:
            case Option.Some(value): return value
            case Option.Not(): raise Exception("called `Option.unwrap()` on a `Not` value")
            case _: unreachable()

    def unwrap_or(self, default: T) -> T:
        match self:
            case Option.Some(value): return value
            case Option.Not(): return default 
            case _: unreachable()

    """
    def unwrap_or_default(self) -> T:
        match self:
            case Option.Some(value): return value
            case Option.Not(): return type(T)()
            case _: unreachable()
    """

    def unwrap_or_else(self, f: Callable[[...], T]) -> T:
        match self:
            case Option.Some(value): return value
            case Option.Not(): return f() 
            case _: unreachable()

def option_convert(f: Callable[[...], T]) -> Callable[[...], Option[T]]:
    def wrapper(*args, **kwargs) -> Option[T]:
        result = f(*args, **kwargs)
        if result is None:
            return Option.Not()
        else:
            return Option.Some(result)

    return wrapper
