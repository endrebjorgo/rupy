from typing import Callable, Self, TypeVar

from .enum import enum, EnumCase
from .option import Option
from .common import unreachable

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")
F = TypeVar("F")

@enum
class Result[T, E]:
    Ok = EnumCase(value=T)
    Err = EnumCase(err=E)

    def is_ok(self) -> bool:
        return self == Result.Ok()

    def is_ok_and(self, f: Callable[[T], bool]) -> bool:
        match self:
            case Result.Ok(value): return f(value)
            case Result.Err(_): return False
            case _: unreachable()

    def is_err(self) -> bool:
        return self == Result.Err()
    
    def is_err_and(self, f: Callable[[T], bool]) -> bool:
        match self:
            case Result.Ok(_): return False
            case Result.Err(err): return f(err)
            case _: unreachable()

    def ok(self) -> Option[T]:
        match self:
            case Result.Ok(value): return Option.Some(value)
            case Result.Err(_): return Option.Not()
            case _: unreachable()

    def err(self) -> Option[E]:
        match self:
            case Result.Ok(_): return Option.Not()
            case Result.Err(err): return Option.Some(err)
            case _: unreachable()

    # def as_ref(self): pass
    # def as_mut(self): pass

    def map(self, op: Callable[[T], U]) -> Self:
        match self:
            case Result.Ok(value): return Result.Ok(op(value))
            case Result.Err(_): return self
            case _: unreachable()

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        match self:
            case Result.Ok(value): return f(value)
            case Result.Err(_): return default 
            case _: unreachable()

    # def map_or_else(self): pass
    # def map_err(self): pass

    def map_err(self, op: Callable[[E], F]) -> Self:
        match self:
            case Result.Ok(_): return self
            case Result.Err(err): return Result.Err(op(err))
            case _: unreachable()

    # def inspect(self): pass
    # def inspect_err(self): pass
    # def as_deref(self): pass
    # def as_deref_mut(self): pass
    # def iter(self): pass
    # def iter_mut(self): pass

    def expect(self, msg: str) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(err): raise Exception(f"{msg}: {err}")
            case _: unreachable()

    def unwrap(self) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(err): raise Exception(f"called `Result.unwrap()` on a `Not` value: \"{err}\"")
            case _: unreachable()

    # def unwrap_or_default(self): pass

    def expect_err(self, msg: str) -> T:
        match self:
            case Result.Ok(value): raise Exception(f"{msg}: {value}")
            case Result.Err(err): return err
            case _: unreachable()

    def unwrap_err(self) -> E:
        match self:
            case Result.Ok(value): raise Exception(value)
            case Result.Err(err): return err
            case _: unreachable()

    def andd(self, res: Self) -> Self:
        match self:
            case Result.Ok(_): return res
            case Result.Err(_): return self
            case _: unreachable()

    def and_then(self, op: Callable[[T], Self]) -> Self:
        match self:
            case Result.Ok(value): return op(value)
            case Result.Err(_): return self
            case _: unreachable()

    def orr(self, res: Self) -> Self:
        match self:
            case Result.Ok(_): return self 
            case Result.Err(_): return res
            case _: unreachable()

    def or_else(self, op: Callable[[E], Self]) -> Self:
        match self:
            case Result.Ok(_): return self
            case Result.Err(err): return op(err)
            case _: unreachable()


    def unwrap_or(self, default: T) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(_): return default 
            case _: unreachable()

    def unwrap_or_else(self, f: Callable[[...], T]) -> T:
        match self:
            case Result.Ok(value): return value
            case Result.Err(_): return f() 
            case _: unreachable()

    # def unwrap_unchecked(self): pass
    # def unwrap_err_unchecked(self): pass

    def convert(f: Callable[[...], T]) -> Callable[[...], Self]:
        def wrapper(*args, **kwargs) -> Result[T, E]:
            try:
                res = f(*args, **kwargs)
                return Result.Ok(res)
            except Exception as e:
                return Result.Err(str(e))

        return wrapper
