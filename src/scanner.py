import string

from tokenclass import *


class Scanner:
    __keywords: dict[str: TokenType] = \
        {"and": TokenType.AND,
         "class": TokenType.CLASS,
         "else": TokenType.ELSE,
         "false": TokenType.FALSE,
         "for": TokenType.FOR,
         "fun": TokenType.FUN,
         "if": TokenType.IF,
         "nil": TokenType.NIL,
         "or": TokenType.OR,
         "print": TokenType.PRINT,
         "return": TokenType.RETURN,
         "super": TokenType.SUPER,
         "this": TokenType.THIS,
         "true": TokenType.TRUE,
         "var": TokenType.VAR,
         "while": TokenType.WHILE
         }

    __digits: str = string.digits
    __letters: str = string.ascii_letters + "_"
    __symbols: str = __letters + __digits

    def __init__(self, source: str, lox_main):
        self.__lox_main = lox_main
        self.__source: str = source
        self.__tokens: list[Token] = []

        self.__token_strings: dict[str, callable] = \
            {"(": lambda _: TokenType.LEFT_PAREN,
             ")": lambda _: TokenType.RIGHT_PAREN,
             "{": lambda _: TokenType.LEFT_BRACE,
             "}": lambda _: TokenType.RIGHT_BRACE,
             ",": lambda _: TokenType.COMMA,
             ".": lambda _: TokenType.DOT,
             "-": lambda _: TokenType.MINUS,
             "+": lambda _: TokenType.PLUS,
             ";": lambda _: TokenType.SEMICOLON,
             "*": lambda _: TokenType.STAR,
             "^": lambda _: TokenType.CARET,
             "%": lambda _: TokenType.PERCENT,
             "!": lambda _: TokenType.BANG_EQUAL if self.__match("=") else TokenType.BANG,
             "=": lambda _: TokenType.EQUAL_EQUAL if self.__match("=") else TokenType.EQUAL,
             "<": lambda _: TokenType.LESS_EQUAL if self.__match("=") else TokenType.LESS,
             ">": lambda _: TokenType.GREATER_EQUAL if self.__match("=") else TokenType.GREATER,
             "/": lambda _: self.__slash_handler(),
             " ": lambda _: None,
             "\t": lambda _: None,
             "\r": lambda _: None,
             "\n": lambda _: self.__newline_handler(),
             "\"": lambda _: self.__string()
             }

        self.__start: int = 0
        self.__current: int = 0
        self.__line: int = 1

    def scan_tokens(self) -> list[Token]:
        while not self.__is_at_end():
            self.__start = self.__current
            self.__scan_token()

        self.__tokens.append(Token(TokenType.EOF, "", None, self.__line))
        return self.__tokens

    def __scan_token(self) -> None:
        c: str = self.__advance()
        if c in self.__token_strings:
            res = self.__token_strings[c](c)
            if res is not None:
                self.__add_simple_token(res)
        elif c in self.__digits:
            self.__number()
        elif c in self.__symbols:
            self.__identifier()
        else:
            self.__lox_main.line_error(self.__line, "Unexpected character.")

    def __add_token(self, typ: TokenType, literal: object | None) -> None:
        text: str = self.__source[self.__start: self.__current]
        self.__tokens.append(Token(typ, text, literal, self.__line))

    def __add_simple_token(self, typ: TokenType) -> None:
        self.__add_token(typ, None)

    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def __advance(self) -> str:
        char: str = self.__source[self.__current]
        self.__current += 1

        return char

    def __match(self, expected: str) -> bool:
        if self.__is_at_end() or self.__source[self.__current] != expected:
            return False

        self.__current += 1
        return True

    def __peek(self) -> str:
        return "\0" if self.__is_at_end() else self.__source[self.__current]

    def __peek_next(self) -> str:
        return "\0" if self.__current + 1 >= len(self.__source) else self.__source[self.__current + 1]

    # Long token handlers

    def __string(self) -> None:
        while self.__peek() != "\"" and not self.__is_at_end():
            if self.__peek == "\n":
                self.__line += 1
            self.__advance()

        if self.__is_at_end():
            self.__lox_main.line_error(self.__line, "Unterminated string.")
            return

        self.__advance()

        value: str = self.__source[self.__start + 1: self.__current - 1]
        self.__add_token(TokenType.STRING, value)

    def __number(self) -> None:
        while self.__peek() in self.__digits:
            self.__advance()

        if self.__peek() == "." and self.__peek_next() in self.__digits:
            self.__advance()
            while self.__peek() in self.__digits:
                self.__advance()

        value: float = float(self.__source[self.__start: self.__current])
        self.__add_token(TokenType.NUMBER, value)

    def __identifier(self) -> None:
        while self.__peek() in self.__symbols:
            self.__advance()

        text: str = self.__source[self.__start: self.__current]
        typ: TokenType = self.__keywords.get(text, TokenType.IDENTIFIER)
        self.__add_simple_token(typ)

    # Special token handlers

    def __slash_handler(self) -> TokenType | None:
        if self.__match("/"):
            while self.__peek() != "\n" and not self.__is_at_end():
                self.__advance()
            return None
        else:
            return TokenType.SLASH

    def __newline_handler(self) -> None:
        self.__line += 1


__all__ = "Scanner",
