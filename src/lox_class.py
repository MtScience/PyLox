from errors import LoxRuntimeError
from lox_callable import LoxCallable
from lox_function import LoxFunction
from tokenclass import Token


class LoxClass(LoxCallable):
    def __init__(self, name: str, superclass, methods: dict[str, LoxFunction]):
        self.name: str = name
        self.superclass: LoxClass | None = superclass
        self.__methods: dict[str, LoxFunction] = methods

    def find_method(self, name: str) -> LoxFunction | None:
        if name in self.__methods:
            return self.__methods.get(name)

        if self.superclass is not None:
            return self.superclass.find_method(name)

        return

    def call(self, interpreter, arguments: list[object]) -> object:
        instance: LoxInstance = LoxInstance(self)
        initializer: LoxFunction = self.find_method("init")
        if initializer is not None:
            initializer.bind(instance).call(interpreter, arguments)

        return instance

    def arity(self) -> int:
        initializer: LoxFunction = self.find_method("init")
        return 0 if initializer is None else initializer.arity()

    def __str__(self) -> str:
        return f"<class {self.name}>"


class LoxInstance:
    def __init__(self, klass: LoxClass):
        self.__klass: LoxClass = klass
        self.__fields: dict[str, object] = {}

    def get(self, name: Token) -> object:
        if name.lexeme in self.__fields:
            return self.__fields.get(name.lexeme)

        method: LoxFunction = self.__klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise LoxRuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name: Token, value: object) -> None:
        self.__fields |= {name.lexeme: value}

    def __str__(self) -> str:
        return f"<{self.__klass.name} instance>"


__all__ = ["LoxClass", "LoxInstance"]
