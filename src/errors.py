from tokenclass import Token


class ParseError(Exception):
    pass


class LoxRuntimeError(Exception):
    def __init__(self, token: Token, message: str):
        self.token: Token = token
        self.message: str = message
        super().__init__(self.message)


class LoxFunctionError(Exception):
    def __init__(self, function: str, message: str):
        self.function = function
        self.message = message
        super().__init__()


__all__ = ["ParseError", "LoxRuntimeError", "LoxFunctionError"]
