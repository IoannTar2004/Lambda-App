from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from application.ports.db_transaction import DBTransaction
from settings import settings

db_url = (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}"
       f"/{settings.DB_NAME}")

async_engine = create_async_engine(db_url, echo=True)

class Base(DeclarativeBase):
       pass

class SqlAlchemyDBTransaction(DBTransaction):

       async_session = async_sessionmaker(async_engine)

       async def __aenter__(self) -> "SqlAlchemyDBTransaction":
              self.session = SqlAlchemyDBTransaction.async_session()
              await self.session.begin()
              return self

       async def __aexit__(self, exc_type, exc_val, exc_tb):
              try:
                     if exc_type:
                            await self.session.rollback()
                     else:
                            await self.session.commit()
              finally:
                     await self.session.close()

       async def get(self, model, model_id):
              return await self.session.get(model, model_id)

       def add(self, base: Base):
              self.session.add(base)

       async def refresh(self, base: Base):
              await self.session.refresh(base)

       def delete(self, base: Base):
              self.session.delete(base)