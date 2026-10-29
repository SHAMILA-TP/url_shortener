from datetime import datetime
from typing import Any

from url_shortener.db.session import SessionLocal
from url_shortener.models.click import Click


async def record_click(ctx: dict[str, Any], url_id: int, clicked_at: datetime) -> None:
    async with SessionLocal() as session:
        session.add(Click(url_id=url_id, clicked_at=clicked_at))
        await session.commit()
