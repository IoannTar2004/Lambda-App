from fastapi import HTTPException

from application.ports.db_transaction import DBTransaction
from domain.models.project import Project


class GetProjectsUsecase:

    def __init__(self, db_transaction: DBTransaction):
        self.db_transaction = db_transaction

    async def get(self, user_id: int, project_id: int):
        async with self.db_transaction as tx:
            project = await tx.get(Project, project_id)

            if not project:
                raise HTTPException(status_code=404, detail="Project doesn't exist")

            if user_id != project.user_id:
                raise HTTPException(status_code=403, detail="Project doesn't belong to this user")

            return project

    async def get_list(self, user_id: int):
        async with self.db_transaction as tx:
            projects = await tx.get_by_filters(Project, user_id=user_id)

            if projects and user_id != projects[0].user_id:
                raise HTTPException(status_code=403, detail="Project doesn't belong to this user")

            return [{"project_id": p.id, "project_name": p.project_name} for p in projects]
