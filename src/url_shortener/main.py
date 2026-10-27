from fastapi import FastAPI

from url_shortener.api.routers import urls

app = FastAPI(title="URL shortener")
app.include_router(urls.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
