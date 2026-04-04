from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.function_handler import FunctionHandler
from domain.models.project import Project
from domain.models.function import Function
from settings import settings


class RollbackProjectUsecase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, user_id: int, project_id: int, hard: bool):
        async with self.db_transaction as tx:
            project_list = await tx.get_by_filters(Project, _joins=["functions", "last_revision"],
                                                       id=project_id, user_id=user_id)
            if not project_list:
                raise HTTPException(status_code=404, detail="Function does not exist")
            project: Project = project_list[0]
            if project.version_number == 0:
                raise HTTPException(status_code=409, detail={
                    "type": "v0",
                    "details": "Cannot rollback. Version number is 0"
                })

            conflict_handlers = []
            for function in project.relations["functions"]:
                handler_list = await tx.get_by_filters(FunctionHandler, function_id=function.id,
                                                  project_version=function.project_version)
                if not handler_list:
                    raise HTTPException(status_code=404, detail="Function handler does not exist")
                handler: FunctionHandler = handler_list[0]

                if function.project_version == function.base_version:
                    conflict_handlers.append({
                        "id": function.id,
                        "name": function.name,
                        "service": function.service,
                        "handler_path": handler.function_path,
                        "handler": handler.function_name
                    })
                    continue

                function.project_version -= 1
                await tx.update(function)
                await tx.delete(handler)

            if conflict_handlers:
                raise HTTPException(status_code=409, detail={
                    "type": "conflict handlers",
                    "details": conflict_handlers
                })

            project.version_number -= 1
            await tx.delete(project.relations["last_revision"])
            project_revision = project.relations["last_revision"]
            await tx.update(project)

            payload = {
                "user_id": project.user_id,
                "project_id": project.id,
                "revision_id": project_revision.id,
            }
            if hard:
                await self.async_req.post("/api/code/zip/delete-with-unzip", "code-service", payload,
                    headers={
                      "Authorization": settings.COMMUNICATION_TOKEN
                    })

            await self.async_req.delete("/api/code/zip/delete-version", "code-service", payload,
                headers={
                    "Authorization": settings.COMMUNICATION_TOKEN
                })
