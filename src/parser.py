from errors import ParseError
from expr import *
from stmt import *
from tokenclass import *


class Parser:
    def __init__(self, tokens: list[Token], lox_main):
        self.__lox_main = lox_main
        self.__current: int = 0
        self.__tokens: list[Token] = tokens

        self.__synchronization_tokens: list[TokenType] = [
            TokenType.CLASS,
            TokenType.FUN,
            TokenType.VAR,
            TokenType.FOR,
            TokenType.IF,
            TokenType.WHILE,
            TokenType.PRINT,
            TokenType.RETURN
        ]

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.__is_at_end():
            statements.append(self.__declaration())

        return statements

    def __statement(self) -> Stmt:
        if self.__match(TokenType.FOR):
            return self.__for_statement()
        if self.__match(TokenType.IF):
            return self.__if_statement()
        if self.__match(TokenType.PRINT):
            return self.__print_statement()
        if self.__match(TokenType.RETURN):
            return self.__return_statement()
        if self.__match(TokenType.WHILE):
            return self.__while_statement()
        if self.__match(TokenType.LEFT_BRACE):
            return BlockStmt(self.__block())

        return self.__expression_statement()

    def __print_statement(self) -> PrintStmt:
        value: Expr = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")

        return PrintStmt(value)

    def __expression_statement(self) -> ExpressionStmt:
        expr: Expr = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after expression.")

        return ExpressionStmt(expr)

    def __if_statement(self) -> IfStmt:
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition: Expr = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        if_clause: Stmt = self.__statement()
        else_clause: Stmt | None = None
        if self.__match(TokenType.ELSE):
            else_clause = self.__statement()

        return IfStmt(condition, if_clause, else_clause)

    def __while_statement(self) -> WhileStmt:
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition: Expr = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body: Stmt = self.__statement()

        return WhileStmt(condition, body)

    def __for_statement(self) -> Stmt:
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer: Stmt | None
        if self.__match(TokenType.SEMICOLON):
            initializer = None
        elif self.__match(TokenType.VAR):
            initializer = self.__var_declaration()
        else:
            initializer = self.__expression_statement()

        condition: Expr | None = None
        if not self.__check(TokenType.SEMICOLON):
            condition = self.__expression()

        self.__consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment: Expr | None = None
        if not self.__check(TokenType.RIGHT_PAREN):
            increment = self.__expression()

        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: Stmt = self.__statement()

        if increment is not None:
            body = BlockStmt([body, ExpressionStmt(increment)])

        if condition is None:
            condition = LiteralExpr(True)
        body = WhileStmt(condition, body)

        if initializer is not None:
            body = BlockStmt([initializer, body])

        return body

    def __function(self, kind: str) -> FunctionStmt:
        name: Token = self.__consume(TokenType.IDENTIFIER, f"Expect {kind} name")

        self.__consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters: list[Token] = []
        if not self.__check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 255:
                    self.__error(self.__peek(), "Can't have more than 255 parameters.")

                parameters.append(self.__consume(TokenType.IDENTIFIER, "Expect parameter name."))

                if not self.__match(TokenType.COMMA):
                    break

        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self.__consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body: list[Stmt] = self.__block()

        return FunctionStmt(name, parameters, body)

    def __return_statement(self) -> ReturnStmt:
        keyword: Token = self.__previous()
        value: Expr | None = None
        if not self.__check(TokenType.SEMICOLON):
            value = self.__expression()

        self.__consume(TokenType.SEMICOLON, "Expect ';' after return value.")

        return ReturnStmt(keyword, value)

    def __declaration(self) -> Stmt | None:
        try:
            if self.__match(TokenType.CLASS):
                return self.__class_declaration()
            if self.__match(TokenType.FUN):
                return self.__function("function")
            if self.__match(TokenType.VAR):
                return self.__var_declaration()
            return self.__statement()
        except ParseError:
            self.__synchronize()
            return

    def __var_declaration(self) -> VarStmt:
        name: Token = self.__consume(TokenType.IDENTIFIER, "Expect a variable name.")

        initializer: Expr | None = None
        if self.__match(TokenType.EQUAL):
            initializer = self.__expression()

        self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return VarStmt(name, initializer)

    def __class_declaration(self) -> ClassStmt:
        name: Token = self.__consume(TokenType.IDENTIFIER, "Expect class name.")

        superclass: VariableExpr | None = None
        if self.__match(TokenType.LESS):
            self.__consume(TokenType.IDENTIFIER, "Expect superclass name.")
            superclass = VariableExpr(self.__previous())

        self.__consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")

        methods: list[FunctionStmt] = []
        while not (self.__check(TokenType.RIGHT_BRACE) or self.__is_at_end()):
            methods.append(self.__function("method"))

        self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")

        return ClassStmt(name, superclass, methods)

    def __assignment(self) -> Expr:
        expr: Expr = self.__or()

        if self.__match(TokenType.EQUAL):
            equals: Token = self.__previous()
            value: Expr = self.__assignment()

            if isinstance(expr, VariableExpr):
                return AssignExpr(expr.name, value)
            elif isinstance(expr, GetExpr):
                return SetExpr(expr.obj, expr.name, value)

            self.__error(equals, "Invalid assignment target.")

        return expr

    def __block(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not (self.__check(TokenType.RIGHT_BRACE) or self.__is_at_end()):
            statements.append(self.__declaration())

        self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def __or(self) -> Expr:
        expr: Expr = self.__and()

        while self.__match(TokenType.OR):
            operator: Token = self.__previous()
            right: Expr = self.__and()
            expr = LogicalExpr(expr, operator, right)

        return expr

    def __and(self) -> Expr:
        expr: Expr = self.__equality()

        while self.__match(TokenType.AND):
            operator: Token = self.__previous()
            right: Expr = self.__equality()
            expr = LogicalExpr(expr, operator, right)

        return expr

    def __expression(self) -> Expr:
        return self.__assignment()

    def __equality(self) -> Expr:
        expr: Expr = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator: Token = self.__previous()
            right: Expr = self.__comparison()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def __comparison(self) -> Expr:
        expr: Expr = self.__term()

        while self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator: Token = self.__previous()
            right: Expr = self.__term()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def __term(self) -> Expr:
        expr: Expr = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator: Token = self.__previous()
            right: Expr = self.__factor()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def __factor(self) -> Expr:
        expr: Expr = self.__power()

        while self.__match(TokenType.SLASH, TokenType.STAR, TokenType.PERCENT):
            operator: Token = self.__previous()
            right: Expr = self.__power()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def __power(self) -> Expr:
        expr: Expr = self.__unary()

        while self.__match(TokenType.CARET):
            operator: Token = self.__previous()
            right: Expr = self.__unary()
            expr = BinaryExpr(expr, operator, right)

        return expr

    def __primary(self) -> Expr:
        if self.__match(TokenType.FALSE):
            return LiteralExpr(False)
        if self.__match(TokenType.TRUE):
            return LiteralExpr(True)
        if self.__match(TokenType.NIL):
            return LiteralExpr(None)
        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.__previous().literal)
        if self.__match(TokenType.SUPER):
            keyword: Token = self.__previous()
            self.__consume(TokenType.DOT, "Expect '.' after 'super'.")
            method: Token = self.__consume(TokenType.IDENTIFIER, "Expect superclass method name.")
            return SuperExpr(keyword, method)
        if self.__match(TokenType.THIS):
            return ThisExpr(self.__previous())
        if self.__match(TokenType.IDENTIFIER):
            return VariableExpr(self.__previous())
        if self.__match(TokenType.LEFT_PAREN):
            expr: Expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        self.__error(self.__peek(), "Expect expression.")

    def __call(self) -> Expr:
        expr: Expr = self.__primary()

        while True:
            if self.__match(TokenType.LEFT_PAREN):
                expr = self.__finish_call(expr)
            elif self.__match(TokenType.DOT):
                name: Token = self.__consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = GetExpr(expr, name)
            else:
                break

        return expr

    def __finish_call(self, callee: Expr) -> Expr:
        arguments: list[Expr] = []

        if not self.__check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 255:
                    self.__lox_main.token_error(self.__peek(), "Can't have more than 255 arguments.")

                arguments.append(self.__expression())
                if not self.__match(TokenType.COMMA):
                    break

        paren = self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")

        return CallExpr(callee, paren, arguments)

    def __unary(self) -> Expr:
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.__previous()
            right: Expr = self.__unary()
            return UnaryExpr(operator, right)

        return self.__call()

    # I know, it's customary in Python to use "*args" for vararg functions and methods, but here I decided to use
    # "*types" to make the definition slightly more readable
    def __match(self, *types) -> bool:
        for typ in types:
            if self.__check(typ):
                self.__advance()
                return True

        return False

    def __check(self, typ: TokenType) -> bool:
        return False if self.__is_at_end() else self.__peek().type == typ

    def __advance(self) -> Token:
        if not self.__is_at_end():
            self.__current += 1

        return self.__previous()

    def __is_at_end(self) -> bool:
        return self.__peek().type == TokenType.EOF

    def __peek(self) -> Token:
        return self.__tokens[self.__current]

    def __previous(self) -> Token:
        return self.__tokens[self.__current - 1]

    def __consume(self, typ: TokenType, message: str) -> Token:
        if self.__check(typ):
            return self.__advance()

        self.__error(self.__peek(), message)

    def __error(self, token: Token, message: str) -> None:
        self.__lox_main.token_error(token, message)
        raise ParseError

    def __synchronize(self) -> None:
        self.__advance()

        while not self.__is_at_end():
            if self.__previous().type == TokenType.SEMICOLON or self.__peek().type in self.__synchronization_tokens:
                return

            self.__advance()


__all__ = "Parser"
