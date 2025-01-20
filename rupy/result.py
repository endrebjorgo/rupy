from typing import TypeVar, Callable

from .enum import enum, EnumCase
from .option import Option
from .common import unreachable

T = TypeVar("T")
E = TypeVar("E")

@enum
class Result[T, E]:
    Ok = EnumCase(value=T)
    Err = EnumCase(err=E)

    def ok(self) -> Option[T]:
        match self:
            case Result.Ok(value): return Option.Some(value)
            case Result.Err(): return Option.Not()
            case _: unreachable()

    def err(self) -> Option[T]:
        match self:
            case Result.Ok(value): return Option.Not()
            case Result.Err(err): return Option.Some(err)
            case _: unreachable()

    def unwrap(self) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(err): raise Exception(f"called `Result.unwrap()` on a `Not` value: \"{err}\"")
            case _: unreachable()

    def unwrap_or(self, default: T) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(): return default 
            case _: unreachable()

    def unwrap_or_else(self, f: Callable[[...], T]) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(): return f() 
            case _: unreachable()

    """
    def unwrap_or_default(self) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(): return type(T)()
            case _: unreachable()
    """

def result_convert(f: Callable[[...], T]) -> Callable[[...], Result[T, E]]:
    def wrapper(*args, **kwargs) -> Result[T, E]:
        try:
            res = f(*args, **kwargs)
            return Result.Ok(res)
        except Exception as e:
            return Result.Err(str(e))

    return wrapper
