# rupy
Library for writing Rust-like Python

## Usage

### Trait, Struct and Impl

Rupy uses class decorators to allow for a similar workflow to Rust with trait 
definitions, struct definitions and implementations blocks.

```python
from rupy import trait, struct, impl

@trait
class Area:
    def area(self): pass

@struct
class Square:
    side_length: float 

@impl(Area)
class Square:
    def area(self) -> float:
        return self.side_length ** 2

circle = Circle(2.0)
assert circle.area() == 4.0
```

### Enum

Rust-like enums with embedded data and structural pattern matching

```python
from rupy import enum, EnumCase

@enum
class Option[T]:
    Some = EnumCase(value=T)
    Not = EnumCase()

match returned_option:
    case Option.Some(val): return val
    case Option.Not(): print("Found nothing")
```

### Result and Option

Built-in Result and Option with easy conversion of pre-existing functions

```python
from rupy import Result

open = Result.convert(open)

content = open("path/to/bad/file", 'r').unwrap_or("BAD FILE")
assert content == "BAD FILE"
```

```python
from rupy import Result

@Option.convert # Added later
def pre_existing_div(a: int, b: int) -> int:
    if b == 0: return None

    return a // b

match pre_existing_div(1, 0):
    case Option.Some(val): ...
    case Option.Not(): ...
```
