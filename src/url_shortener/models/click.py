from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from url_shortener.db.base import Base


class Click(Base):
    __tablename__ = "clicks"
    id: Mapped[int] = mapped_column(primary_key=True)
    url_id: Mapped[int] = mapped_column(
        ForeignKey("urls.id", ondelete="CASCADE"), index=True
    )
    clicked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
