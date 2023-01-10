class Return(Exception):
    def __init__(self, value: object | None):
        super().__init__()
        self.value = value


__all__ = "Return"
