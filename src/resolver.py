from collections import deque
from enum import Enum, auto

from expr import *
from stmt import *
from tokenclass import Token


class ClassType(Enum):
    NONE = auto()
    CLASS = auto()
    SUBCLASS = auto()


class FunctionType(Enum):
    NONE = auto()
    FUNCTION = auto()
    INITIALIZER = auto()
    METHOD = auto()


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter, lox_main):
        self.__lox_main = lox_main
        self.__interpreter = interpreter
        self.__scopes: deque[dict[str, bool]] = deque()
        self.__current_function: FunctionType = FunctionType.NONE
        self.__current_class: ClassType = ClassType.NONE

    def resolve(self, statements: list[Stmt]) -> None:
        for statement in statements:
            self.__resolve_stmt(statement)

    def visit_assign_expr(self, expr: AssignExpr) -> None:
        self.__resolve_expr(expr.value)
        self.__resolve_local(expr, expr.name)

    def visit_binary_expr(self, expr: BinaryExpr) -> None:
        self.__resolve_expr(expr.left)
        self.__resolve_expr(expr.right)

    def visit_call_expr(self, expr: CallExpr) -> None:
        self.__resolve_expr(expr.callee)

        for argument in expr.arguments:
            self.__resolve_expr(argument)

    def visit_get_expr(self, expr: GetExpr) -> None:
        self.__resolve_expr(expr.obj)

    def visit_grouping_expr(self, expr: GroupingExpr) -> None:
        self.__resolve_expr(expr.expression)

    @staticmethod
    def visit_literal_expr(expr: LiteralExpr) -> None:
        pass

    def visit_logical_expr(self, expr: LogicalExpr) -> None:
        self.__resolve_expr(expr.left)
        self.__resolve_expr(expr.right)

    def visit_set_expr(self, expr: SetExpr) -> None:
        self.__resolve_expr(expr.value)
        self.__resolve_expr(expr.obj)

    def visit_super_expr(self, expr: SuperExpr) -> None:
        if self.__current_class == ClassType.NONE:
            self.__lox_main.token_error(expr.keyword, "Can't use 'super' outside of a class.")
        elif self.__current_class != ClassType.SUBCLASS:
            self.__lox_main.token_error(expr.keyword, "Can't use 'super' in a class with no superclass.")

        self.__resolve_local(expr, expr.keyword)

    def visit_this_expr(self, expr: ThisExpr) -> None:
        if self.__current_class == ClassType.NONE:
            self.__lox_main.token_error(expr.keyword, "Can't use 'this' outside of a class.")
            return

        self.__resolve_local(expr, expr.keyword)

    def visit_unary_expr(self, expr: UnaryExpr) -> None:
        self.__resolve_expr(expr.right)

    def visit_variable_expr(self, expr: VariableExpr) -> None:
        # Comparing as "is False" because "get" can return None, which is also false, but shouldn't satisfy the
        # condition
        if len(self.__scopes) != 0 and self.__scopes[-1].get(expr.name.lexeme) is False:
            self.__lox_main.token_error(expr.name, "Can't read local variable in its own initializer.")

        self.__resolve_local(expr, expr.name)

    def visit_block_stmt(self, stmt: BlockStmt) -> None:
        self.__begin_scope()
        self.resolve(stmt.statements)
        self.__end_scope()

    def visit_class_stmt(self, stmt: ClassStmt) -> None:
        enclosing_class: ClassType = self.__current_class
        self.__current_class = ClassType.CLASS

        self.__declare(stmt.name)
        self.__define(stmt.name)

        if stmt.superclass is not None:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                self.__lox_main.token_error(stmt.superclass.name, "A class can't inherit from itself.")

            self.__current_class = ClassType.SUBCLASS
            self.__resolve_expr(stmt.superclass)

            self.__begin_scope()
            self.__scopes[-1] |= {"super": True}

        self.__begin_scope()
        self.__scopes[-1] |= {"this": True}

        for method in stmt.methods:
            declaration: FunctionType = \
                FunctionType.INITIALIZER if method.name.lexeme == "init" else FunctionType.METHOD
            self.__resolve_function(method, declaration)

        self.__end_scope()

        if stmt.superclass is not None:
            self.__end_scope()

        self.__current_class = enclosing_class

    def visit_expression_stmt(self, stmt: ExpressionStmt) -> None:
        self.__resolve_expr(stmt.expression)

    def visit_function_stmt(self, stmt: FunctionStmt) -> None:
        self.__declare(stmt.name)
        self.__define(stmt.name)

        self.__resolve_function(stmt, FunctionType.FUNCTION)

    def visit_if_stmt(self, stmt: IfStmt) -> None:
        self.__resolve_expr(stmt.condition)
        self.__resolve_stmt(stmt.if_clause)
        if stmt.else_clause is not None:
            self.__resolve_stmt(stmt.else_clause)

    def visit_print_stmt(self, stmt: PrintStmt) -> None:
        self.__resolve_expr(stmt.expression)

    def visit_return_stmt(self, stmt: ReturnStmt) -> None:
        if self.__current_function == FunctionType.NONE:
            self.__lox_main.token_error(stmt.keyword, "Can't return from top-level code.")

        if stmt.value is not None:
            if self.__current_function == FunctionType.INITIALIZER:
                self.__lox_main.token_error(stmt.keyword, "Can't return a value from an initializer.")
            self.__resolve_expr(stmt.value)

    def visit_var_stmt(self, stmt: VarStmt) -> None:
        self.__declare(stmt.name)
        if stmt.initializer is not None:
            self.__resolve_expr(stmt.initializer)

        self.__define(stmt.name)

    def visit_while_stmt(self, stmt: WhileStmt) -> None:
        self.__resolve_expr(stmt.condition)
        self.__resolve_stmt(stmt.body)

    # TODO: check if it is possible to combine the two private "resolve" methods, since except for argument types
    #  they're identical
    def __resolve_expr(self, expr: Expr) -> None:
        expr.accept(self)

    def __resolve_stmt(self, stmt: Stmt) -> None:
        stmt.accept(self)

    def __resolve_local(self, expr: Expr, name: Token) -> None:
        for i in range(len(self.__scopes) - 1, -1, -1):
            if name.lexeme in self.__scopes[i]:
                self.__interpreter.resolve(expr, len(self.__scopes) - 1 - i)
                return

    def __resolve_function(self, function: FunctionStmt, typ: FunctionType) -> None:
        enclosing_function: FunctionType = self.__current_function
        self.__current_function = typ

        self.__begin_scope()
        for param in function.params:
            self.__declare(param)
            self.__define(param)

        self.resolve(function.body)
        self.__end_scope()
        self.__current_function = enclosing_function

    def __begin_scope(self) -> None:
        self.__scopes.append({})

    def __end_scope(self) -> None:
        self.__scopes.pop()

    def __declare(self, name: Token) -> None:
        if len(self.__scopes) == 0:
            return

        scope: dict[str, bool] = self.__scopes[-1]
        if name.lexeme in scope:
            self.__lox_main.token_error(name, "Already a variable with this name in this scope.")

        scope |= {name.lexeme: False}

    def __define(self, name: Token) -> None:
        if len(self.__scopes) == 0:
            return

        self.__scopes[-1] |= {name.lexeme: True}


__all__ = "Resolver"
