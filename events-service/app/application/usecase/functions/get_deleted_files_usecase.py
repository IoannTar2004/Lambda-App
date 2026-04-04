from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from domain.models.function import Function
from domain.models.function_handler import FunctionHandler
from infrastructure.database.sqlalchemy_db_transaction import SqlAlchemyDBTransaction
from settings import settings


class GetDeletedFilesUsecase:

    def __init__(self, db_transaction: SqlAlchemyDBTransaction, async_req: AsyncRequest):
        self.db_transaction = db_transaction
        self.async_req = async_req

    async def execute(self, user_id: int, project_id: int):
        project_files = await self.async_req.get("/api/code/file/listdir-all", "code-service",
                                                 params={
                                                     "bucket": "user-code",
                                                     "path": f"{user_id}/{project_id}"
                                                 },
                                                 headers={
                                                     "Authorization": settings.COMMUNICATION_TOKEN
                                                 })

        project_files = [f["Key"] for f in project_files]

        async with self.db_transaction as tx:
            functions: list[Function]= await tx.get_by_filters(Function, _joins=["handler"], project_id=project_id)

            deleted = []
            for function in functions:
                handler: FunctionHandler = function.relations["handler"]
                full_path = f"{user_id}/{project_id}/{handler.function_path}"
                if full_path not in project_files:
                    deleted.append({
                        "id": handler.function_id,
                        "handlerPath": handler.function_path,
                        "handler": handler.function_name
                    })

            return deleted
