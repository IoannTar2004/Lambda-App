from dataclasses import asdict

from sqlalchemy import update, select, delete, inspect, text
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import selectinload, joinedload

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

    async def get_by_filters(self, domain_class, _selections: list[str] | None = None,
                             _joins: list[str] | None = None, **kwargs):
        model_class = DOMAIN_MODEL_MAPPING[domain_class]
        filters = []
        for k, v in kwargs.items():
            column = getattr(model_class, k)

            if isinstance(v, (list, tuple)):
                if not v:
                    filters.append(column is None)
                    continue
                filters.append(column.in_(v))
            else:
                filters.append(column == v)

        options = []
        requested_relations = []
        if _selections:
            options += [selectinload(getattr(model_class, name)) for name in _selections]
            requested_relations += _selections
        if _joins:
            options += [joinedload(getattr(model_class, name)) for name in _joins]
            requested_relations += _joins

        result = await self.session.execute(
            select(model_class).where(*filters).options(*options)
        )

        return [model_to_domain(res_domain, requested_relations) for res_domain in result.scalars().unique().all()]

    async def get_by_query(self, domain_class, sql: str, **kwargs):
        model_class = DOMAIN_MODEL_MAPPING[domain_class]
        query = select(model_class).from_statement(text(sql))
        result = await self.session.execute(query, kwargs)

        return [model_to_domain(res_domain) for res_domain in result.scalars().all()]

    async def insert(self, domain):
        model = domain_to_model(domain)
        self.session.add(model)
        await self.session.flush()
        return model_to_domain(model)

    async def update(self, domain):
        model_class = DOMAIN_MODEL_MAPPING[type(domain)]
        data = asdict(domain)
        data.pop("relations", None)
        data.pop("id", None)

        await self.session.execute(
            update(model_class)
            .where(model_class.id == domain.id)
            .values(**data)
        )

    async def delete(self, domain):
        model_class = DOMAIN_MODEL_MAPPING[type(domain)]
        await self.session.execute(
            delete(model_class).where(model_class.id == domain.id)
        )

    async def delete_by_filters(self, domain_class, **kwargs):
        model_class = DOMAIN_MODEL_MAPPING[domain_class]
        filters = [getattr(model_class, k) == v for k, v in kwargs.items()]
        await self.session.execute(
            delete(model_class).where(*filters)
        )