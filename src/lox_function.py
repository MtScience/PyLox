from environment import Environment
from lox_callable import LoxCallable
from return_class import Return
from stmt import FunctionStmt


class LoxFunction(LoxCallable):
    def __init__(self, declaration: FunctionStmt, closure: Environment):
        self.__declaration: FunctionStmt = declaration
        self.__closure: Environment = closure

    def bind(self, instance):
        environment: Environment = Environment(self.__closure)
        environment.define("this", instance)

        return LoxFunction(self.__declaration, environment)

    def call(self, interpreter, arguments: list[object]) -> object:
        environment: Environment = Environment(self.__closure)

        # A tiny sprinkle of Haskell-like functional programming:
        for param, argument in zip(self.__declaration.params, arguments):
            environment.define(param.lexeme, argument)

        try:
            interpreter.execute_block(self.__declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return

    def arity(self) -> int:
        return len(self.__declaration.params)

    def __str__(self) -> str:
        return f"<fn {self.__declaration.name.lexeme}>"


__all__ = "LoxFunction"
