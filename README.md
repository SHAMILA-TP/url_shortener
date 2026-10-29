# URL Shortener

I built this to learn Python and FastAPI coming from Rails. You give it a long URL, it gives back a short link, and opening that link sends you to the original page. Every visit is counted in the background, so the redirect stays instant.

## What it does

- Create a short link, with an optional custom code and an optional expiry date
- Redirect from the short link (expired or unknown links return 404)
- Record each click through a Redis job queue, so it never slows down the redirect

## Built with

Python 3.13 · FastAPI · PostgreSQL · SQLAlchemy 2.0 (async) · Alembic · Pydantic v2 · Redis + Arq · Docker Compose

## How it's organized

Requests go **router → service → repository → database**. Routers only deal with HTTP, services hold the rules (code generation, expiry, reserved words), and repositories hold the SQL. Clicks go **redirect → Redis → worker → database**.

## Run it

```bash
uv sync
cp .env.example .env              # set DATABASE_URL and REDIS_URL
docker compose up -d              # Redis
uv run alembic upgrade head       # create tables
uv run uvicorn url_shortener.main:app --reload    # API
uv run arq url_shortener.worker.WorkerSettings    # worker (second terminal)
```

API docs: http://127.0.0.1:8000/docs

## Still to do

Tests, logging, a stats endpoint, and handling Redis being down.
