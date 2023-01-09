from abc import ABC, abstractmethod

from expr import Expr
from tokenclass import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor): ...


class StmtVisitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: Stmt): ...

    @abstractmethod
    def visit_expression_stmt(self, stmt: Stmt): ...

    @abstractmethod
    def visit_if_stmt(self, stmt: Stmt): ...

    @abstractmethod
    def visit_print_stmt(self, stmt: Stmt): ...

    @abstractmethod
    def visit_var_stmt(self, stmt: Stmt): ...

    @abstractmethod
    def visit_while_stmt(self, stmt: Stmt): ...


class BlockStmt(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements: list[Stmt] = statements

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_block_stmt(self)


class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_expression_stmt(self)


class IfStmt(Stmt):
    def __init__(self, condition: Expr, if_clause: Stmt, else_clause: Stmt | None):
        self.condition: Expr = condition
        self.if_clause: Stmt = if_clause
        self.else_clause: Stmt | None = else_clause

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_if_stmt(self)


class PrintStmt(Stmt):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_print_stmt(self)


class VarStmt(Stmt):
    def __init__(self, name: Token, initializer: Expr):
        self.name: Token = name
        self.initializer: Expr = initializer

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_var_stmt(self)


class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Stmt):
        self.condition: Expr = condition
        self.body: Stmt = body

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_while_stmt(self)


__all__ = ["Stmt", "StmtVisitor", "BlockStmt", "ExpressionStmt", "IfStmt", "PrintStmt", "VarStmt", "WhileStmt"]
