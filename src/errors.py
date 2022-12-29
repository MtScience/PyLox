from tokenclass import Token


class ParseError(Exception):
    pass


class LoxRuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        self.token: Token = token
        self.message: str = message
        super().__init__(self.message)


__all__ = ["ParseError", "LoxRuntimeError"]
