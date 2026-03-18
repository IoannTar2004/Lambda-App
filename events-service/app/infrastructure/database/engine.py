from sqlalchemy.ext.asyncio import create_async_engine

from settings import settings

db_url = (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"
       f"/{settings.DB_NAME}")

async_engine = create_async_engine(db_url, echo=True)
