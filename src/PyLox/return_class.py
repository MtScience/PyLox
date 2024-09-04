class Return(Exception):
    def __init__(self, value: object | None):
        super().__init__()
        self.value: object | None = value


__all__ = "Return",
