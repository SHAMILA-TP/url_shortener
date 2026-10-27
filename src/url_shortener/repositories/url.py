from datetime import datetime

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener.core.exceptions import ShortCodeTakenError
from url_shortener.models.url import Url


class UrlRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_short_code(self, code: str) -> Url | None:
        result = await self.session.execute(select(Url).where(Url.short_code == code))
        return result.scalar_one_or_none()

    async def create(
        self, short_code: str, original_url: str, expires_at: datetime | None
    ) -> Url:
        url = Url(
            short_code=short_code, original_url=original_url, expires_at=expires_at
        )
        try:
            async with self.session.begin_nested():
                self.session.add(url)
                await self.session.flush()
        except IntegrityError as exc:
            raise ShortCodeTakenError(short_code) from exc
        return url
