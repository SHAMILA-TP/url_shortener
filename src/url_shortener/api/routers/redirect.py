from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from url_shortener.api.deps import get_session
from url_shortener.services.url import UrlService

router = APIRouter(tags=["redirect"])


@router.get("/{code}")
async def redirect_to_url(
    code: str,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> RedirectResponse:
    destination = await UrlService(session).resolve(code)
    return RedirectResponse(url=destination, status_code=307)
