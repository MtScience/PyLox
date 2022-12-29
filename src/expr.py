from abc import ABC, abstractmethod

from tokenclass import Token


class Expr(ABC):
    @abstractmethod
    def accept(self, visitor): ...


class BinaryExpr(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left: Expr = left
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: Expr):
        return visitor.visit_binary_expr(self)


class GroupingExpr(Expr):
    def __init__(self, expr: Expr):
        self.expr: Expr = expr

    def accept(self, visitor: Expr):
        return visitor.visit_grouping_expr(self)


class LiteralExpr(Expr):
    def __init__(self, value: object):
        self.value: object = value

    def accept(self, visitor: Expr):
        return visitor.visit_literal_expr(self)


class UnaryExpr(Expr):
    def __init__(self, operator: Token, right: Expr):
        self.operator: Token = operator
        self.right: Expr = right

    def accept(self, visitor: Expr):
        return visitor.visit_unary_expr(self)


__all__ = ["Expr", "BinaryExpr", "GroupingExpr", "LiteralExpr", "UnaryExpr"]
