from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.function_handler import FunctionHandler
from domain.models.project import Project
from domain.models.function import Function
from domain.models.project_revision import ProjectRevision
from settings import settings


class CommitProjectUseCase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, user_id: int, data: dict):
        async with self.db_transaction as tx:
            project: Project = await tx.get(Project, data["project_id"])
            if not project:
                raise HTTPException(status_code=404, detail="Project doesn't exist")
            if project.user_id != user_id:
                raise HTTPException(status_code=403, detail="Project doesn't belong to user")

            project.version_number += 1
            await tx.update(project)

            project_revision = ProjectRevision(project.id, project.version_number)
            project_revision = await tx.insert(project_revision)

            function_list = await tx.get_by_filters(Function, _joins=['handler'], project_id=data["project_id"],
                                                    user_id=user_id)

            update_handlers_dict = data["functions"]
            for function in function_list:
                handler: FunctionHandler = function.relations["handler"]
                if not handler:
                    raise HTTPException(status_code=404, detail="Handler not found")

                function.project_version += 1
                await tx.update(function)
                new_handler = FunctionHandler(function_id=function.id,
                                              project_version=function.project_version,
                                              memory_size=handler.memory_size,
                                              timeout=handler.timeout,
                                              function_path=handler.function_path,
                                              function_name=handler.function_name)

                if function.id in update_handlers_dict:
                    new_handler.function_path = update_handlers_dict[function.id]["function_path"]
                    new_handler.function_name = update_handlers_dict[function.id]["function_name"]

                await tx.insert(new_handler)

            await self.async_req.post("/api/code/zip/zip-project", "code-service", {
                "user_id": project.user_id,
                "project_id": project.id,
                "revision_id": project_revision.id
            }, headers={
                "Authorization": settings.COMMUNICATION_TOKEN
            }) # TODO заменить все на Kafka