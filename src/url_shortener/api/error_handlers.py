from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from url_shortener.core.exceptions import (
    AppError,
    CodeGenerationError,
    InvalidCustomCodeError,
    InvalidExpiryError,
    ShortCodeTakenError,
    UrlNotFoundError,
)

STATUS_BY_ERROR: dict[type[AppError], int] = {
    ShortCodeTakenError: status.HTTP_409_CONFLICT,
    InvalidCustomCodeError: status.HTTP_422_UNPROCESSABLE_CONTENT,
    InvalidExpiryError: status.HTTP_422_UNPROCESSABLE_CONTENT,
    CodeGenerationError: status.HTTP_503_SERVICE_UNAVAILABLE,
    UrlNotFoundError: status.HTTP_404_NOT_FOUND,
}


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    status_code = STATUS_BY_ERROR.get(type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
