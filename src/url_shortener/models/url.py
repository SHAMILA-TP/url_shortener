from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from url_shortener.db.base import Base

if TYPE_CHECKING:
    from url_shortener.models.click import Click


class Url(Base):
    __tablename__ = "urls"
    clicks: Mapped[list["Click"]] = relationship(
        back_populates="url", passive_deletes=True
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    short_code: Mapped[str] = mapped_column(String(32), unique=True)
    original_url: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
