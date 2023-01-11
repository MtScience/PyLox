from errors import LoxRuntimeError
from tokenclass import Token


class Environment:
    def __init__(self, enclosing=None):
        self.values: dict[str, object] = {}
        self.enclosing: Environment | None = enclosing

    def ancestor(self, distance: int):
        environment: Environment = self
        for _ in range(distance):
            environment = environment.enclosing

        return environment

    def assign(self, name: Token, value: object) -> None:
        if name.lexeme in self.values:
            self.values |= {name.lexeme: value}
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def assign_at(self, distance: int, name: Token, value: object) -> None:
        self.ancestor(distance).values |= {name.lexeme: value}

    def define(self, name: str, value: object) -> None:
        self.values |= {name: value}

    def get(self, name: Token) -> object:
        if name.lexeme in self.values:
            return self.values.get(name.lexeme)

        if self.enclosing is not None:
            return self.enclosing.get(name)

        raise LoxRuntimeError(name, f"Undefined variable '{name.lexeme}'.")

    def get_at(self, distance: int, name: str) -> object:
        return self.ancestor(distance).values.get(name)
