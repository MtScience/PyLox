import time

from lox_callable import LoxCallable


class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments: list[object]) -> float:
        return time.time()

    def __str__(self) -> str:
        return "<native fn>"


__all__ = ["Clock"]
