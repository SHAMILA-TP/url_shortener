import re
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener.core.exceptions import (
    CodeGenerationError,
    InvalidCustomCodeError,
    InvalidExpiryError,
    ShortCodeTakenError,
    UrlNotFoundError,
)
from url_shortener.models.url import Url
from url_shortener.repositories.url import UrlRepository
from url_shortener.services.short_code import generate_short_code

# Paths the app itself uses; a short code with these names would be unreachable.
RESERVED_CODES = frozenset({"api", "docs", "redoc", "openapi.json", "health", "admin"})
CUSTOM_CODE_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,32}$")
MAX_GENERATION_ATTEMPTS = 5


class UrlService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = UrlRepository(session)

    async def create_short_url(
        self,
        original_url: str,
        custom_code: str | None,
        expires_at: datetime | None,
    ) -> Url:
        if expires_at is not None and expires_at <= datetime.now(timezone.utc):
            raise InvalidExpiryError("expires_at must be in the future")

        if custom_code is not None:
            self._validate_custom_code(custom_code)
            url = await self.repo.create(custom_code, original_url, expires_at)
        else:
            url = await self._create_with_generated_code(original_url, expires_at)

        await self.session.commit()
        return url

    async def _create_with_generated_code(
        self, original_url: str, expires_at: datetime | None
    ) -> Url:
        for _ in range(MAX_GENERATION_ATTEMPTS):
            try:
                return await self.repo.create(
                    generate_short_code(), original_url, expires_at
                )
            except ShortCodeTakenError:
                continue
        raise CodeGenerationError("Could not generate a unique short code")

    @staticmethod
    def _validate_custom_code(code: str) -> None:
        if not CUSTOM_CODE_PATTERN.fullmatch(code):
            raise InvalidCustomCodeError(
                "custom_code must be 3-32 characters: letters, digits, '_' or '-'"
            )
        if code.lower() in RESERVED_CODES:
            raise InvalidCustomCodeError(f"'{code}' is a reserved word")

    async def resolve(self, code: str) -> str:
        url = await self.repo.get_by_short_code(code)
        if url is None or (
            url.expires_at is not None and url.expires_at <= datetime.now(timezone.utc)
        ):
            raise UrlNotFoundError(f"No active link for '{code}'")
        return url.original_url
