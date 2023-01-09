from enum import Enum, auto
from typing import SupportsFloat

from environment import Environment
from errors import LoxRuntimeError
from expr import *
from stmt import *
from tokenclass import *


class OpMode(Enum):
    SCRIPT = auto()
    INTERACTIVE = auto()


class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self, lox_main):
        self.__lox_main = lox_main
        self.__environment: Environment = Environment()

        self.__unary_operators: dict[TokenType, callable] = {
            TokenType.MINUS: self.__unary_minus_handler,
            TokenType.BANG: lambda _, x: not self.__is_truthy(x)
        }
        self.__binary_operators: dict[TokenType, callable] = {
            TokenType.MINUS: self.__binary_minus_handler,
            TokenType.PLUS: self.__binary_plus_handler,
            TokenType.SLASH: self.__binary_slash_handler,
            TokenType.STAR: self.__binary_star_handler,
            TokenType.CARET: self.__binary_caret_handler,
            TokenType.GREATER: self.__binary_gtr_handler,
            TokenType.GREATER_EQUAL: self.__binary_geq_handler,
            TokenType.LESS: self.__binary_less_handler,
            TokenType.LESS_EQUAL: self.__binary_leq_handler,
            TokenType.BANG_EQUAL: lambda _, l, r: not self.__is_equal(l, r),
            TokenType.EQUAL_EQUAL: lambda _, l, r: self.__is_equal(l, r)
        }

    def interpret(self, statements: list[Stmt], mode: OpMode) -> None:
        try:
            for statement in statements:
                self.__mode_execute(statement, mode)
        except LoxRuntimeError as err:
            self.__lox_main.runtime_error(err)

    @staticmethod
    def visit_literal_expr(expr: LiteralExpr) -> object:
        return expr.value

    def visit_grouping_expr(self, expr: GroupingExpr) -> object:
        return self.__evaluate(expr.expr)

    def visit_binary_expr(self, expr: BinaryExpr) -> object | bool:
        left: object = self.__evaluate(expr.left)
        right: object = self.__evaluate(expr.right)

        return self.__binary_operators[expr.operator.type](expr.operator, left, right)

    def visit_unary_expr(self, expr: UnaryExpr) -> object:
        right: object = self.__evaluate(expr.right)

        return self.__unary_operators[expr.operator.type](expr.operator, right)

    def visit_variable_expr(self, expr: VariableExpr) -> object:
        return self.__environment.get(expr.name)

    def visit_assign_expr(self, expr: AssignExpr) -> object:
        value: object = self.__evaluate(expr.value)
        self.__environment.assign(expr.name, value)
        return value

    def visit_block_stmt(self, stmt: BlockStmt) -> None:
        self.execute_block(stmt.statements, Environment(self.__environment))

    def visit_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self.__evaluate(stmt.expression)

    def visit_print_stmt(self, stmt: PrintStmt) -> None:
        value: object = self.__evaluate(stmt.expression)
        print(self.__stringify(value))

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        value: object | None = None
        if stmt.initializer is not None:
            value = self.__evaluate(stmt.initializer)

        self.__environment.define(stmt.name.lexeme, value)

    def visit_if_stmt(self, stmt: IfStmt) -> None:
        if self.__is_truthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.if_clause)
        elif stmt.else_clause is not None:
            self.__execute(stmt.else_clause)

    def __mode_execute(self, stmt: Stmt, mode: OpMode) -> None:
        if mode == OpMode.INTERACTIVE and isinstance(stmt, ExpressionStmt):
            value: object = self.__evaluate(stmt.expression)
            print(self.__stringify(value))
        else:
            self.__execute(stmt)

    def __evaluate(self, expr: Expr) -> object:
        return expr.accept(self)

    def __execute(self, stmt: Stmt) -> None:
        return stmt.accept(self)

    def execute_block(self, statements: list[Stmt], environment: Environment) -> None:
        previous: Environment = self.__environment
        try:
            self.__environment = environment
            for statement in statements:
                self.__execute(statement)
        finally:
            self.__environment = previous

    @staticmethod
    def __is_truthy(obj: object) -> bool:
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj

        return True

    @staticmethod
    def __is_equal(a: object, b: object) -> bool:
        if a is None and b is None:
            return True
        if a is None:
            return False

        return a == b

    @staticmethod
    def __check_number_operand(operator: Token, operand: object) -> None:
        if isinstance(operand, float):
            return

        raise LoxRuntimeError(operator, "Operand must be a number.")

    @staticmethod
    def __check_number_operands(operator: Token, left: object, right: object) -> None:
        if isinstance(left, float) and isinstance(right, float):
            return

        raise LoxRuntimeError(operator, "Operands must be numbers.")

    @staticmethod
    def __stringify(obj: object) -> str:
        if obj is True:
            return "true"
        if obj is False:
            return "false"
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text: str = str(obj)
            if text.endswith(".0"):
                text = text[:-2]
            return text

        return str(obj)

    @staticmethod
    def __binary_plus_handler(operator: Token, left: object, right: object) -> float | str:
        if isinstance(left, float) and isinstance(right, float):
            return float(left) + float(right)

        if isinstance(left, str) and isinstance(right, str):
            return str(left) + str(right)

        raise LoxRuntimeError(operator, "Operands must be two numbers or two strings.")

    def __binary_minus_handler(self, operator: Token, left: SupportsFloat, right: SupportsFloat) -> float:
        self.__check_number_operands(operator, left, right)
        return float(left) - float(right)

    def __binary_slash_handler(self, operator: Token, left: SupportsFloat, right: SupportsFloat) -> float:
        self.__check_number_operands(operator, left, right)
        return float(left) / float(right)

    def __binary_star_handler(self, operator: Token, left: SupportsFloat, right: SupportsFloat) -> float:
        self.__check_number_operands(operator, left, right)
        return float(left) * float(right)

    def __binary_caret_handler(self, operator: Token, left: SupportsFloat, right: SupportsFloat) -> float:
        self.__check_number_operands(operator, left, right)
        return float(left) ** float(right)

    def __binary_gtr_handler(self, operator: Token, left: SupportsFloat, right: SupportsFloat) -> bool:
        self.__check_number_operands(operator, left, right)
        return float(left) > float(right)

    def __binary_geq_handler(self, operator: Token, left: SupportsFloat, right: SupportsFloat) -> bool:
        self.__check_number_operands(operator, left, right)
        return float(left) >= float(right)

    def __binary_less_handler(self, operator: Token, left: SupportsFloat, right: SupportsFloat) -> bool:
        self.__check_number_operands(operator, left, right)
        return float(left) < float(right)

    def __binary_leq_handler(self, operator: Token, left: SupportsFloat, right: SupportsFloat) -> bool:
        self.__check_number_operands(operator, left, right)
        return float(left) <= float(right)

    def __unary_minus_handler(self, operator: Token, x: SupportsFloat) -> float:
        self.__check_number_operand(operator, x)
        return -float(x)


__all__ = ["Interpreter", "OpMode"]
