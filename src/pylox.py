import sys

from errors import LoxRuntimeError
from interpreter import *
from parser import Parser
from scanner import Scanner
from stmt import Stmt
from tokenclass import *


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
        scanner: Scanner = Scanner(source, self)
        tokens: list[Token] = scanner.scan_tokens()

        parser: Parser = Parser(tokens, self)
        statements: list[Stmt] = parser.parse()

        if self.had_error:
            return

        self.__interpreter.interpret(statements, mode)

    def run_repl(self) -> None:
        while True:
            try:
                line = input("> ")
            except EOFError:
                print()
                break

            self.__run(line, OpMode.INTERACTIVE)

    def run_file(self, path: str) -> None:
        with open(path, "r") as file:
            code = file.read()

        self.__run(code, OpMode.SCRIPT)

        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)


if __name__ == '__main__':
    if (length := len(sys.argv)) > 2:
        print("Usage: pylox [script]")
        sys.exit(64)
    elif length == 2:
        Lox().run_file(sys.argv[1])
    else:
        Lox().run_repl()
