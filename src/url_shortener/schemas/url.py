from datetime import datetime

from pydantic import AwareDatetime, BaseModel, ConfigDict, HttpUrl


class UrlCreate(BaseModel):
    url: HttpUrl
    custom_code: str | None = None
    expires_at: AwareDatetime | None = None


class UrlRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    short_code: str
    original_url: str
    created_at: datetime
    expires_at: datetime | None
