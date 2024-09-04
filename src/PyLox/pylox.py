import sys

from .errors import LoxRuntimeError
from .interpreter import *
from .parser import Parser
from .resolver import Resolver
from .scanner import Scanner
from .stmt import Stmt
from .tokenclass import *


class Lox:
    def __init__(self):
        self.__interpreter: Interpreter = Interpreter(self)
        self.had_error: bool = False
        self.had_runtime_error: bool = False

    def token_error(self, token: Token, message: str) -> None:
        where: str = " at end" if token.type == TokenType.EOF else f" at '{token.lexeme}'"
        self.__report(token.line, where, message)

    def line_error(self, line: int, message: str) -> None:
        self.__report(line, "", message)

    def runtime_error(self, err: LoxRuntimeError) -> None:
        print(f"Error: {err.message}\n[line {err.token.line}]", file=sys.stderr)
        self.had_runtime_error = True

    def __report(self, ln: int, where: str, msg: str) -> None:
        print(f"[line {ln}] Error{where}: {msg}", file=sys.stderr)
        self.had_error = True

    def __run(self, source: str, mode: OpMode) -> None:
        tokens: list[Token] = Scanner(source, self).scan_tokens()
        statements: list[Stmt] = Parser(tokens, self).parse()

        if self.had_error:
            return

        Resolver(self.__interpreter, self).resolve(statements)

        if self.had_error:
            return

        self.__interpreter.interpret(statements, mode)

    def run_repl(self) -> None:
        while True:
            try:
                line = input("> ")
            except (EOFError, KeyboardInterrupt):
                print()
                break

            self.__run(line, OpMode.INTERACTIVE)
            self.had_error = False  # Unset error flag to allow for printing after errors in REPL

    def run_file(self, path: str) -> None:
        with open(path, "rt", encoding="utf-8") as file:
            code = file.read()

        self.__run(code, OpMode.SCRIPT)

        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)
