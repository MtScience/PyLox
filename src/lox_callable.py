from abc import ABC, abstractmethod


class LoxCallable(ABC):
    @ abstractmethod
    def arity(self) -> int: ...

    @abstractmethod
    def call(self, interpreter, arguments: list[object]) -> object: ...

    @abstractmethod
    def __str__(self) -> str: ...


__all__ = "LoxCallable"
