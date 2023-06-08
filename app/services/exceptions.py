class InvalidTableSize(Exception):
    """Недопустимый размер таблицы."""

    def __init__(
            self,
            message: str,
            status_code: int = None
    ):
        super().__init__()
        self.message = message
        if status_code:
            self.status_code = status_code
