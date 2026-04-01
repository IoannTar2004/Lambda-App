from dataclasses import dataclass
from typing import Any

from fastapi import HTTPException
from sqlalchemy.util import await_only

from application.ports.db_transaction import DBTransaction
from domain.models.function import Function


class GetFunctionsUsecase:

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

    async def get_all(self, user_id: int) -> list[dict]:
        async with self.db_transaction as tx:
            functions : list[Function] = await tx.get_by_filters(Function, _joins=["handler"], user_id=user_id)

            if functions and functions[0].user_id != user_id:
                raise HTTPException(status_code=403, detail="Functions don't belong to this user")

            return [{
                "id": f.id,
                "name": f.name,
                "service": f.service,
                "project_version": f.project_version,
                "environment": f.environment,
                "handler_path": f.relations["handler"].function_path,
                "handler": f.relations["handler"].function_name,
                "memory_size": f.relations["handler"].memory_size,
                "timeout": f.relations["handler"].timeout,
                "created_at": f.created_at
            } for f in functions]