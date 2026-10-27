from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener.db.session import SessionLocal


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
