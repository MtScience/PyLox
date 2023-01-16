import math
import time
from abc import ABC, abstractmethod

from errors import LoxFunctionError
from lox_callable import LoxCallable
from lox_class import *
from lox_function import LoxFunction


class LoxNativeFunction(LoxCallable, ABC):
    @abstractmethod
    def __init__(self):
        self.name: str | None = None

    @abstractmethod
    def arity(self) -> int: ...

    @abstractmethod
    def call(self, interpreter, arguments: list[object]) -> object: ...

    def __str__(self) -> str:
        return "<native fn>"


class Clock(LoxNativeFunction):
    def __init__(self):
        self.name: str = "clock"

    def arity(self) -> int:
        return 0

    def call(self, interpreter, _: list[object]) -> float:
        return time.time()


class GetLine(LoxNativeFunction):
    def __init__(self):
        self.name: str = "getline"

    def arity(self) -> int:
        return 0

    def call(self, interpreter, _: list[object]) -> str:
        return input()


class Type(LoxNativeFunction):
    def __init__(self):
        self.name: str = "type"

    def arity(self) -> int:
        return 1

    def call(self, interpreter, arguments: list[object]) -> str:
        obj: object = arguments[0]

        if isinstance(obj, bool):
            return "boolean"
        elif isinstance(obj, float):
            return "number"
        elif isinstance(obj, str):
            return "string"
        elif isinstance(obj, (LoxFunction, LoxNativeFunction)):
            return "function"
        elif isinstance(obj, LoxClass):
            return "class"
        elif isinstance(obj, LoxInstance):
            return obj.klass.name
        elif obj is None:
            return "nil"

        return str(obj)


class ToString(LoxNativeFunction):
    def __init__(self):
        self.name: str = "tostring"

    def arity(self) -> int:
        return 1

    def call(self, interpreter, arguments: list[object]) -> str:
        obj: object = arguments[0]

        if isinstance(obj, LoxNativeFunction):
            return f"fn <{obj.name}>"

        return str(obj)


class ToNumber(LoxNativeFunction):
    def __init__(self):
        self.name: str = "tonumber"

    def arity(self) -> int:
        return 1

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: object = arguments[0]

        if not isinstance(obj, str):
            raise LoxFunctionError(self.name, "Expect type 'string'")

        try:
            return float(obj)
        except ValueError:
            raise LoxFunctionError(self.name, "The string doesn't represent a valid number")


# Mathematical functions

class MathFunction(LoxNativeFunction, ABC):
    @abstractmethod
    def __init__(self):
        self.name: str | None = None

    def arity(self) -> int:
        return 1

    def check_number(self, argument: object) -> float | None:
        if not isinstance(argument, float):
            raise LoxFunctionError(self.name, "Expect type 'number'")

        return argument

    @abstractmethod
    def call(self, interpreter, arguments: list[object]) -> object: ...


class Exponent(MathFunction):
    def __init__(self):
        self.name: str = "exp"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.exp(obj)


class Logarithm(MathFunction):
    def __init__(self):
        self.name: str = "log"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.log(obj)


class ToRadians(MathFunction):
    def __init__(self):
        self.name: str = "rad"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.radians(obj)


class Sine(MathFunction):
    def __init__(self):
        self.name: str = "sin"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.sin(obj)


class ArcSine(MathFunction):
    def __init__(self):
        self.name: str = "asin"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.asin(obj)


class Cosine(MathFunction):
    def __init__(self):
        self.name: str = "cos"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.cos(obj)


class ArcCosine(MathFunction):
    def __init__(self):
        self.name: str = "acos"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.acos(obj)


class Tangent(MathFunction):
    def __init__(self):
        self.name: str = "tan"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.tan(obj)


class ArcTangent(MathFunction):
    def __init__(self):
        self.name: str = "atan"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.atan(obj)


class Ceiling(MathFunction):
    def __init__(self):
        self.name: str = "ceil"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.ceil(obj)


class Floor(MathFunction):
    def __init__(self):
        self.name: str = "floor"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return math.floor(obj)


class Round(MathFunction):
    def __init__(self):
        self.name: str = "round"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return round(obj)


class Absolute(MathFunction):
    def __init__(self):
        self.name = "abs"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])
        return abs(obj)


class Sign(MathFunction):
    def __init__(self):
        self.name: str = "sign"

    def call(self, interpreter, arguments: list[object]) -> float:
        obj: float = self.check_number(arguments[0])

        if obj == 0:
            return 0
        elif obj > 0:
            return 1
        return -1


native_functions: list = [Clock, GetLine, Type, ToString, ToNumber, Exponent, Logarithm, ToRadians, Sine, Cosine,
                          Tangent, ArcSine, ArcCosine, ArcTangent, Ceiling, Floor, Round, Absolute, Sign]

__all__ = ["LoxNativeFunction", "native_functions"]
