from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException
from sqlalchemy.util import await_only

from application.ports.db_transaction import DBTransaction
from domain.models.function import Function
from domain.models.s3_function import S3Function


class GetFunctionsUsecase:

    service_domain = {
        "S3": S3Function
    }

    def __init__(self, db_transaction: DBTransaction):
        self.db_transaction = db_transaction

    async def get(self, user_id: int, function_id: int) -> dict[str, Any]:
        async with self.db_transaction as tx:
            functions = await tx.get_by_filters(Function, _joins=["handler"], id=function_id)

            if not functions:
                raise HTTPException(status_code=404, detail="Function doesn't exist")

            function: Function = functions[0]
            if user_id != function.user_id:
                raise HTTPException(status_code=403, detail="Function doesn't belong to this user")

            service_info = await self._get_service_information(function.service, function.id, tx)
            return self._get_function_response(function) | service_info

    async def get_all(self, user_id: int, project_id: int) -> list[dict]:
        async with self.db_transaction as tx:
            functions : list[Function] = await tx.get_by_filters(Function, _joins=["handler"], project_id=project_id)
            if not functions:
                return []
            if functions and functions[0].user_id != user_id:
                raise HTTPException(status_code=403, detail="Functions don't belong to this user")

            return [self._get_function_response(f) | await self._get_service_information(f.service, f.id, tx)
                    for f in functions]


    def _get_function_response(self, function):
        return {
            "id": function.id,
            "name": function.name,
            "service": function.service,
            "project_version": function.project_version,
            "environment": function.environment,
            "handler_path": function.relations["handler"].function_path,
            "handler": function.relations["handler"].function_name,
            "memory_size": function.relations["handler"].memory_size,
            "timeout": function.relations["handler"].timeout,
            "created_at": function.created_at
        }

    async def _get_service_information(self, service, id, tx):
        domain = GetFunctionsUsecase.service_domain[service]
        result = await tx.get(domain, id)
        result_dict = result.__dict__

        result_dict.pop("id")
        result_dict.pop("relations")

        return result_dict