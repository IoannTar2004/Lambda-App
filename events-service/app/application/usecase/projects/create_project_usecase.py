from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from domain.models.project import Project


class CreateProjectUsecase:

    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction):
        self.async_req = async_req
        self.db_transaction = db_transaction

    async def execute(self, user_id: int, project_name: str):
        async with self.db_transaction as tx:
            project = Project(user_id, project_name, 1)
            project = await tx.insert(project)

            await self.async_req.post("/api/zip/zip-project", "code-service", {
                "user_id": project.user_id,
                "project_id": project.id,
                "project_name": project.project_name,
                "version_number": project.version_number
            })  # TODO заменить все на Kafka

        return {
            "project_id": project.id
        }
