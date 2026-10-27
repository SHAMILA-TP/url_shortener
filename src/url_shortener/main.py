from fastapi import FastAPI

app = FastAPI(title="URL shortener")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
