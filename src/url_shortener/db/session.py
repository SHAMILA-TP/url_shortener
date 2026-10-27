from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from url_shortener.core.config import get_settings

engine = create_async_engine(get_settings().database_url)
# build the connection pool using the db url in the .env file through settings
# engine        = the pool of connections (once per app)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
# session       = borrows a connection from the pool for one request, each session local gives a fresh session that borrows a connection from engine
