from fastapi import FastAPI

from url_shortener.api.error_handlers import register_exception_handlers
from url_shortener.api.routers import redirect, urls

app = FastAPI(title="URL shortener")
register_exception_handlers(app)
app.include_router(urls.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


# Registered last: "/{code}" matches any single path segment, so it must not shadow the routes above.
app.include_router(redirect.router)
