from lox_callable import LoxCallable


class LoxClass(LoxCallable):
    def __init__(self, name: str):
        self.name: str = name

    def call(self, interpreter, arguments: list[object]) -> object:
        instance: LoxInstance = LoxInstance(self)
        return instance

    def arity(self) -> int:
        return 0

    def __str__(self) -> str:
        return f"<class {self.name}>"


class LoxInstance:
    def __init__(self, klass: LoxClass):
        self.__klass: LoxClass = klass

    def __str__(self) -> str:
        return f"<{self.__klass.name} instance>"


__all__ = ["LoxClass", "LoxInstance"]
