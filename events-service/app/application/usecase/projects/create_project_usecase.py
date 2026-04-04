import io

from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.project import Project
from settings import settings


class CreateProjectUsecase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, user_id: int, project_name: str):
        async with self.db_transaction as tx:
            exist_project = await tx.get_by_filters(Project, project_name=project_name, user_id=user_id)
            if exist_project:
                raise HTTPException(status_code=409, detail="Project already exists")

            project = Project(user_id, project_name)
            project = await tx.insert(project)

        return {
            "project_id": project.id
        }
