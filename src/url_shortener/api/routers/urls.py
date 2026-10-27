from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener.api.deps import get_session
from url_shortener.models.url import Url
from url_shortener.schemas.url import UrlCreate, UrlRead
from url_shortener.services.url import UrlService

router = APIRouter(prefix="/api/urls", tags=["urls"])


@router.post("", response_model=UrlRead, status_code=status.HTTP_201_CREATED)
async def create_url(
    payload: UrlCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Url:
    service = UrlService(session)
    return await service.create_short_url(
        original_url=str(payload.url),
        custom_code=payload.custom_code,
        expires_at=payload.expires_at,
    )
