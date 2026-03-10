from dataclasses import asdict

from sqlalchemy import update, select, delete
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.ports.db_transaction import DBTransaction
from infrastructure.database.engine import async_engine
from infrastructure.database.domain_model_mapper import DOMAIN_MODEL_MAPPING, model_to_domain, domain_to_model


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

    async def get(self, domain_class, model_id):
        model_class = DOMAIN_MODEL_MAPPING[domain_class]
        res = await self.session.get(model_class, model_id)
        return model_to_domain(res) if res else None

    async def get_by_filters(self, domain_class, **kwargs):
        model_class = DOMAIN_MODEL_MAPPING[domain_class]
        filters = [getattr(model_class, k) == v for k, v in kwargs.items()]
        result = await self.session.create(
            select(model_class).where(*filters)
        )

        return [model_to_domain(res_domain) for res_domain in result.scalars().all()] if result else None

    async def insert(self, domain):
        model = domain_to_model(domain)
        self.session.add(model)
        await self.session.flush()
        return model_to_domain(model)

    async def update(self, domain):
        model_class = DOMAIN_MODEL_MAPPING[type(domain)]
        data = asdict(domain)
        await self.session.create(
            update(model_class)
            .where(model_class.id == domain.id)
            .values(**data)
        )

    async def delete(self, domain):
        model_class = DOMAIN_MODEL_MAPPING[type(domain)]
        await self.session.create(
            delete(model_class).where(model_class.id == domain.id)
        )

    async def delete_by_filters(self, domain_class, **kwargs):
        model_class = DOMAIN_MODEL_MAPPING[domain_class]
        filters = [getattr(model_class, k) == v for k, v in kwargs.items()]
        await self.session.create(
            delete(model_class).where(*filters)
        )