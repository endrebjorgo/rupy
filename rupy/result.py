from typing import TypeVar, Callable

from .enum import enum, EnumCase
from .option import Option

T = TypeVar("T")
E = TypeVar("E")

@enum
class Result[T, E]:
    Ok = EnumCase(value=T)
    Err = EnumCase(msg=E)

    def ok(self) -> Option[T]:
        match self:
            case Result.Ok(value): return Option.Some(value)
            case Result.Err(e): return Option.Not()

    def unwrap(self) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(msg): raise Exception(msg)

    def unwrap_or(self, default: T) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err: return default 

    def unwrap_or_else(self, f: Callable[[...], T]) -> T:
        match self:
            case Result.Ok(value): return value
            case _: return f() 

    """
    def unwrap_or_default(self) -> T:
        match self:
            case Option.Some(value): return value
            case _: return type(T)()
    """

def result_convert(f: Callable[[...], T]) -> Callable[[...], Result[T, E]]:
    def wrapper(*args, **kwargs) -> Result[T, E]:
        try:
            res = f(*args, **kwargs)
            return Result.Ok(res)
        except Exception as e:
            return Result.Err(str(e))

    return wrapper
