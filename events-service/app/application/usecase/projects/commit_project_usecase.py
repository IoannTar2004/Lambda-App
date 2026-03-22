from fastapi import HTTPException

from application.commands.update_function_command import UpdateProjectCommand
from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.project import Project
from domain.models.function import Function


class CommitProjectUseCase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, user_id: int, project_id: int):
        async with self.db_transaction as tx:
            project: Project = await tx.get(Project, project_id)
            if not project:
                raise HTTPException(status_code=404, detail="Project doesn't exist")
            if project.user_id != user_id:
                raise HTTPException(status_code=403, detail="Project doesn't belong to user")

            project.version_number += 1
            await tx.update(project)

            await self.async_req.post("/api/zip/zip-project", "code-service", {
                "user_id": project.user_id,
                "project_name": project.project_name,
                "version_number": project.version_number
            }) # TODO заменить все на Kafka