from environment import Environment
from lox_callable import LoxCallable
from stmt import FunctionStmt


class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt):
        self.__declaration = declaration

    def call(self, interpreter, arguments: list[object]) -> object:
        environment: Environment = Environment(interpreter.globals)

        # A tiny sprinkle of Haskell-like functional programming:
        for param, argument in zip(self.__declaration.params, arguments):
            environment.define(param.lexeme, argument)

        interpreter.execute_block(self.__declaration.body, environment)
        return

    def arity(self) -> int:
        return len(self.__declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.__declaration.name.lexeme}>"


__all__ = "LoxFunction"
