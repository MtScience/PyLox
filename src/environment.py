from errors import LoxRuntimeError
from tokenclass import Token


class Environment:
    def __init__(self, enclosing=None):
        self.__values: dict[str, object] = {}
        self.enclosing: Environment | None = enclosing

    def define(self, name: str, value: object) -> None:
        self.__values |= {name: value}

    def get(self, name: Token) -> object:
        if name.lexeme in self.__values:
            return self.__values.get(name.lexeme)

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.__values:
            self.__values |= {name.lexeme: value}
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
