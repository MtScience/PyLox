from abc import ABC, abstractmethod

from expr import Expr
from tokenclass import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor): ...


class BlockStmt(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements: list[Stmt] = statements

    def accept(self, visitor: Stmt):
        return visitor.visit_block_stmt(self)


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


class VarStmt(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name: Token = name
        self.initializer: Expr = initializer

    def accept(self, visitor: Stmt):
        return visitor.visit_var_stmt(self)


__all__ = ["Stmt", "BlockStmt", "ExpressionStmt", "PrintStmt", "VarStmt"]
