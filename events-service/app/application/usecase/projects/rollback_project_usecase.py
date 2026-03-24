from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.function_handler import FunctionHandler
from domain.models.project import Project
from domain.models.function import Function


class RollbackProjectUsecase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, user_id: int, project_id: int):
        async with self.db_transaction as tx:
            project_list = await tx.get_by_filters(Project, _joins=["functions"],
                                                       id=project_id, user_id=user_id)
            if not project_list:
                raise HTTPException(status_code=404, detail="Function does not exist")
            project: Project = project_list[0]
            if project.version_number == 1:
                raise HTTPException(status_code=409, detail="Cannot rollback. Version number is 1")

            prev_version = project.version_number
            project.version_number -= 1
            await tx.update(project)

            for function in project.relations["functions"]:
                handler_list = await tx.get_by_filters(FunctionHandler, function_id=function.id,
                                                  project_version=function.project_version)
                if not handler_list:
                    raise HTTPException(status_code=404, detail="Function handler does not exist")
                handler = handler_list[0]

                function.project_version -= 1
                await tx.update(function)
                await tx.delete(handler)

            await self.async_req.delete("/api/zip/delete-version", "code-service", {
                "user_id": project.user_id,
                "project_id": project.id,
                "version_number": prev_version
            }) # TODO заменить на kafka
