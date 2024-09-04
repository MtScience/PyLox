from abc import ABC, abstractmethod

from .tokenclass import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor): ...


# "None" as output type was added for the Resolver class, since at resolution pass expressions don't produce values,
# but they do at runtime
class ExprVisitor(ABC):
    @abstractmethod
    def visit_assign_expr(self, expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_binary_expr(self, expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_call_expr(self, expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_get_expr(self, expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_grouping_expr(self, expr: Expr) -> object | None: ...

    @staticmethod
    @abstractmethod
    def visit_literal_expr(expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_logical_expr(self, expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_set_expr(self, expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_super_expr(self, expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_this_expr(self, expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_unary_expr(self, expr: Expr) -> object | None: ...

    @abstractmethod
    def visit_variable_expr(self, expr: Expr) -> object | None: ...


class AssignExpr(Expr):
    def __init__(self, name: Token, value: Expr):
        self.name: Token = name
        self.value: Expr = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_assign_expr(self)


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)


class CallExpr(Expr):
    def __init__(self, callee: Expr, paren: Token, arguments: list[Expr]):
        self.callee: Expr = callee
        self.paren: Token = paren
        self.arguments: list[Expr] = arguments

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_call_expr(self)


class GetExpr(Expr):
    def __init__(self, obj: Expr, name: Token):
        self.obj: Expr = obj
        self.name: Token = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_get_expr(self)


class GroupingExpr(Expr):
    def __init__(self, expression: Expr):
        self.expression: Expr = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping_expr(self)


class LiteralExpr(Expr):
    def __init__(self, value: object):
        self.value: object = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal_expr(self)


class LogicalExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_logical_expr(self)


class SetExpr(Expr):
    def __init__(self, obj: Expr, name: Token, value: Expr):
        self.obj: Expr = obj
        self.name: Token = name
        self.value: Expr = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_set_expr(self)


class SuperExpr(Expr):
    def __init__(self, keyword: Token, method: Token):
        self.keyword: Token = keyword
        self.method: Token = method

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_super_expr(self)


class ThisExpr(Expr):
    def __init__(self, keyword: Token):
        self.keyword: Token = keyword

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_this_expr(self)


class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary_expr(self)


class VariableExpr(Expr):
    def __init__(self, name: Token):
        self.name: Token = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_variable_expr(self)


__all__ = ("Expr", "ExprVisitor", "AssignExpr", "BinaryExpr", "CallExpr", "GetExpr", "GroupingExpr",
           "LiteralExpr", "LogicalExpr", "SetExpr", "SuperExpr", "ThisExpr", "UnaryExpr", "VariableExpr")
