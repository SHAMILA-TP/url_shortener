from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI

from url_shortener.api.error_handlers import register_exception_handlers
from url_shortener.api.routers import redirect, urls
from url_shortener.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    app.state.redis = await create_pool(
        RedisSettings.from_dsn(get_settings().redis_url)
    )
    yield
    await app.state.redis.aclose()


app = FastAPI(title="URL shortener", lifespan=lifespan)
register_exception_handlers(app)
app.include_router(urls.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Registered last: "/{code}" matches any single path segment, so it must not shadow the routes above.
app.include_router(redirect.router)
