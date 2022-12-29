from expr import *
from tokenclass import *


class AstPrinter:
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary_expr(self, expr: BinaryExpr) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: GroupingExpr) -> str:
        return self.__parenthesize("group", expr.expr)

    @staticmethod
    def visit_literal_expr(expr: LiteralExpr) -> str:
        return "nil" if expr.value is None else str(expr.value)

    def visit_unary_expr(self, expr: UnaryExpr) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def __parenthesize(self, name: str, *exprs) -> str:
        string: list[str] = [f"{expr.accept(self)}" for expr in exprs]
        string: str = f"({name} " + " ".join(string) + ")"

        return string


if __name__ == '__main__':
    expr: BinaryExpr = BinaryExpr(
        UnaryExpr(
            Token(TokenType.MINUS, "-", None, 1),
            LiteralExpr(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        GroupingExpr(LiteralExpr(45.67))
    )

    print(AstPrinter().print(expr))
