import sys

from errors import LoxRuntimeError
from interpreter import *
from parser import Parser
from resolver import Resolver
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
        tokens: list[Token] = Scanner(source, self).scan_tokens()
        statements: list[Stmt] = Parser(tokens, self).parse()

        if self.had_error:
            return

        Resolver(self.__interpreter, self).resolve(statements)

        if self.had_error:
            return

        self.__interpreter.interpret(statements, mode)

    def __run_options(self, options: dict) -> None:
        if options is None:
            return

        if "-e" in options:
            self.__run(options["-e"], OpMode.SCRIPT)

    def run_repl(self, options: dict = None) -> None:
        self.__run_options(options)

        while True:
            try:
                line = input("> ")
            except EOFError:
                print()
                break

            self.__run(line, OpMode.INTERACTIVE)
            self.had_error = False  # Unset error flag to allow for printing after errors in REPL

    def run_file(self, path: str, options: dict = None) -> None:
        with open(path, "rt", encoding="utf-8") as file:
            code = file.read()

        self.__run_options(options)
        self.__run(code, OpMode.SCRIPT)

        if self.had_error:
            sys.exit(65)
        if self.had_runtime_error:
            sys.exit(70)

        if options is not None and "-i" in options:
            self.run_repl()


def print_usage() -> None:
    usage: str = "usage: python pylox.py [options] [script]\n\n" \
                 "Available options:\n"\
                 " -h        show this message and exit\n"\
                 " -e str    run string 'str'\n"\
                 " -i        enter interactive mode\n"
    print(usage)


def collect_options(given: list) -> tuple[dict, str | None]:
    i: int = 0
    options: dict = {}
    script: str | None = None

    while i < (length := len(given)):
        match given[i]:
            case "-i" | "-h": options |= {given[i]: None}
            case "-e":
                i += 1
                if i >= length or given[i].startswith("-"):
                    print(f"'-e' requires an argument")
                    print_usage()
                    sys.exit(64)
                options |= {"-e": given[i]}
            case _ if given[i].startswith("-"):
                print(f"unrecognized option: '{given[i]}'")
                print_usage()
                sys.exit(64)
            case _:
                script = given[i]
                break
        i += 1

    return options, script


if __name__ == "__main__":
    options: dict
    script: str | None
    options, script = collect_options(sys.argv[1:])

    if "-h" in options:
        print_usage()
        sys.exit()

    if script is not None:
        Lox().run_file(script, options)
    else:
        Lox().run_repl(options)
