from errors import LoxRuntimeError
from tokenclass import Token


class Environment:
    def __init__(self):
        self.__values: dict[str, object] = {}

    def define(self, name: str, value: object) -> None:
        self.__values |= {name: value}

    def get(self, name: Token) -> object:
        if name.lexeme in self.__values:
            return self.__values.get(name.lexeme)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.__values:
            self.__values |= {name.lexeme: value}
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")
