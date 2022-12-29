from abc import ABC, abstractmethod

from expr import Expr
from tokenclass import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor): ...


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Stmt):
        return visitor.visit_expression_stmt(self)


class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: Stmt):
        return visitor.visit_print_stmt(self)


__all__ = ["Stmt", "ExpressionStmt", "PrintStmt"]