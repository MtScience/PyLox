from abc import ABC, abstractmethod

from .expr import Expr, VariableExpr
from .tokenclass import Token


class Stmt(ABC):
    @abstractmethod
    def accept(self, visitor): ...


# All "visit_<type>_stmt" methods shouldn't produce output since statements don't produce values
class StmtVisitor(ABC):
    @abstractmethod
    def visit_block_stmt(self, stmt: Stmt) -> None: ...

    @abstractmethod
    def visit_expression_stmt(self, stmt: Stmt) -> None: ...

    @abstractmethod
    def visit_function_stmt(self, stmt: Stmt) -> None: ...

    @abstractmethod
    def visit_if_stmt(self, stmt: Stmt) -> None: ...

    @abstractmethod
    def visit_print_stmt(self, stmt: Stmt) -> None: ...

    @abstractmethod
    def visit_return_stmt(self, stmt: Stmt) -> None: ...

    @abstractmethod
    def visit_var_stmt(self, stmt: Stmt) -> None: ...

    @abstractmethod
    def visit_while_stmt(self, stmt: Stmt) -> None: ...

    @abstractmethod
    def visit_class_stmt(self, stmt: Stmt) -> None: ...


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


class FunctionStmt(Stmt):
    def __init__(self, name: Token, params: list[Token], body: list[Stmt]):
        self.name: Token = name
        self.params: list[Token] = params
        self.body: list[Stmt] = body

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_function_stmt(self)


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


class ReturnStmt(Stmt):
    def __init__(self, keyword: Token, value: Expr | None):
        self.keyword: Token = keyword
        self.value: Expr | None = value

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_return_stmt(self)


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


class ClassStmt(Stmt):
    def __init__(self, name: Token, superclass: VariableExpr | None, methods: list[FunctionStmt]):
        self.name: Token = name
        self.superclass: VariableExpr | None = superclass
        self.methods: list[FunctionStmt] = methods

    def accept(self, visitor: StmtVisitor):
        return visitor.visit_class_stmt(self)


__all__ = ("Stmt", "StmtVisitor", "BlockStmt", "ExpressionStmt", "FunctionStmt",
           "IfStmt", "PrintStmt", "ReturnStmt", "VarStmt", "WhileStmt", "ClassStmt")
