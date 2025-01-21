from typing import Callable, Self, TypeVar

from .enum import enum, EnumCase
from .common import unreachable

T = TypeVar("T")
E = TypeVar("E")
U = TypeVar("U")

@enum
class Option[T]:
    Some = EnumCase(value=T)
    Not = EnumCase()

    def is_some(self) -> bool:
        return self == Option.Some()

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        match self:
            case Option.Some(value): return f(value)
            case Option.Not(): return False
            case _: unreachable()

    def is_none(self) -> bool:
        return self == Option.Not()
    
    def is_none_or(self, f: Callable[[T], bool]) -> bool:
        match self:
            case Option.Some(value): return f(value)
            case Option.Not(): return True
            case _: unreachable()

    # def as_ref(self): pass
    # def as_mut(self): pass
    # def as_pin_ref(self): pass
    # def as_pin_mut(self): pass
    # def as_pin(self): pass
    # def as_mut_slice(self): pass

    def expect(self, msg: str) -> T:
        match self:
            case Option.Some(value): return value
            case Option.Not(): raise Exception(msg)
            case _: unreachable()

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

    def unwrap_or_else(self, f: Callable[[...], T]) -> T:
        match self:
            case Option.Some(value): return value
            case Option.Not(): return f() 
            case _: unreachable()

    # def unwrap_or_default(self): pass
    # def unwrap_unchecked(self): pass

    def map(self, f: Callable[[T], U]) -> Self:
        match self:
            case Option.Some(value): return Option.Some(f(value))
            case Option.Not(): return self
            case _: unreachable()

    # def inspect(self): pass

    def map_or(self, default: U, f: Callable[[T], U]) -> U:
        match self:
            case Option.Some(value): return f(value)
            case Option.Not(): return default 
            case _: unreachable()

    # def map_or_else(self): pass
    # def ok_or(self, err: E): pass
    # def ok_or_else(self): pass
    # def as_deref(self): pass
    # def as_deref_mut(self): pass
    # def iter(self): pass
    # def iter_mut(self): pass

    def andd(self, optb: Self) -> Self:
        match self:
            case Option.Some(_): return optb
            case Option.Not(): return self
            case _: unreachable()

    def and_then(self, f: Callable[[T], Self]) -> Self:
        match self:
            case Option.Some(value): return f(value)
            case Option.Not(): return self
            case _: unreachable()

    def filter(self, f: Callable[[T], bool]) -> Self:
        match self:
            case Option.Some(value): return self if f(value) else Option.Not()
            case Option.Not(): return self
            case _: unreachable()

    def orr(self, optb: Self) -> Self:
        match self:
            case Option.Some(value): return self 
            case Option.Not(): return optb
            case _: unreachable()

    def or_else(self, f: Callable[[...], Self]) -> Self:
        match self:
            case Option.Some(value): return self
            case Option.Not(): return f()
            case _: unreachable()


    def xor(self, optb: Self) -> Self:
        match self:
            case Option.Some(_):
                match optb:
                    case Option.Some(_): return Option.Not()
                    case Option.Not(): return self
                    case _: unreachable()
            case Option.Not(): 
                match optb:
                    case Option.Some(_): return optb
                    case Option.Not(): return self
                    case _: unreachable()
            case _: unreachable()


    # def insert(self): pass
    # def get_or_insert(self): pass
    # def get_or_insert_default(self): pass
    # def get_or_insert_with(self): pass
    # def take(self): pass
    # def take_if(self): pass
    # def replace(self): pass
    # def zip(self): pass
    # def zip_with(self): pass

    def convert(f: Callable[[...], T]) -> Callable[[...], Self]:
        def wrapper(*args, **kwargs) -> Option[T]:
            result = f(*args, **kwargs)
            if result is None:
                return Option.Not()
            else:
                return Option.Some(result)

        return wrapper
