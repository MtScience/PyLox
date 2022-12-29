from errors import ParseError
from expr import *
from tokenclass import *


class Parser:
    def __init__(self, tokens: list[Token], lox_main):
        self.__lox_main = lox_main
        self.__current: int = 0
        self.__tokens: list[Token] = tokens

        self.__synchronization_tokens: list[TokenType] = \
            [TokenType.CLASS,
             TokenType.FUN,
             TokenType.VAR,
             TokenType.FOR,
             TokenType.IF,
             TokenType.WHILE,
             TokenType.PRINT,
             TokenType.RETURN
             ]

    def parse(self) -> Expr | None:
        try:
            return self.__expression()
        except ParseError:
            return

    def __expression(self) -> Expr:
        # return self.__assignment()
        return self.__equality()

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

        while self.__match(TokenType.SLASH, TokenType.STAR):
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

    def __unary(self) -> Expr:
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator: Token = self.__previous()
            right: Expr = self.__unary()
            return UnaryExpr(operator, right)
          
        return self.__primary()

    def __primary(self) -> Expr:
        if self.__match(TokenType.FALSE):
            return LiteralExpr(False)
        if self.__match(TokenType.TRUE):
            return LiteralExpr(True)
        if self.__match(TokenType.NIL):
            return LiteralExpr(None)
        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return LiteralExpr(self.__previous().literal)
        if self.__match(TokenType.LEFT_PAREN):
            expr: Expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return GroupingExpr(expr)

        self.__error(self.__peek(), "Expect expression.")

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
