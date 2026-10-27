class AppError(Exception):
    """Base class for errors the API turns into HTTP responses."""


class ShortCodeTakenError(AppError):
    def __init__(self, short_code: str) -> None:
        super().__init__(f"Short code already in use: {short_code}")
        self.short_code = short_code


class InvalidCustomCodeError(AppError):
    pass


class InvalidExpiryError(AppError):
    pass


class CodeGenerationError(AppError):
    pass


class UrlNotFoundError(AppError):
    pass
