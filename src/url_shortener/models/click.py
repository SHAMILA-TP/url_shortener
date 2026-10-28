from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from url_shortener.db.base import Base

if TYPE_CHECKING:
    from url_shortener.models.url import Url


class Click(Base):
    __tablename__ = "clicks"
    url: Mapped["Url"] = relationship(back_populates="clicks")
    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(
        ForeignKey("urls.id", ondelete="CASCADE"), index=True
    )
    clicked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
