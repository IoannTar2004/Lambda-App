from fastapi import HTTPException

from application.ports.async_request import AsyncRequest
from application.ports.db_transaction import DBTransaction
from application.ports.storage_notification import StorageNotification
from application.usecase.specific_functions.s3_function_usecase import S3FunctionUsecase
from domain.models.function import Function
from domain.models.project import Project
from domain.models.s3_function import S3Function
from settings import settings


class DeleteProjectUsecase:
    def __init__(self, async_req: AsyncRequest, db_transaction: DBTransaction, storage_notification: StorageNotification):
        self.db_transaction = db_transaction
        self.async_req = async_req
        self.storage_notification = storage_notification

    async def execute(self, user_id: int, project_id: int):
        async with self.db_transaction as tx:
            projects = await tx.get_by_filters(Project, _limit=1, _joins=["functions"], id=project_id)
            if not projects:
                raise HTTPException(status_code=404, detail="Project not found")
            project: Project = projects[0]
            if project.user_id != user_id:
                raise HTTPException(status_code=403, detail="Project doesn't belong to this user")

            functions: list[Function] = project.relations["functions"]
            for function in functions:
                match function.service:
                    case "S3":
                        await self._delete_s3_events(function.id, tx)

            await self.async_req.delete("/api/code/file/delete-all", "code-service",
                params={
                    "bucket": "user-code",
                    "path": f"{user_id}/{project_id}"
                },
                headers={
                    "Authorization": settings.COMMUNICATION_TOKEN
                }
            )

            await self.async_req.delete("/api/code/file/delete-all", "code-service",
                params={
                    "bucket": "code-archives",
                    "path": f"{user_id}/{project_id}"
                },
                headers={
                    "Authorization": settings.COMMUNICATION_TOKEN
                }
            )

            await tx.delete(project)

    async def _delete_s3_events(self, id: int, tx: DBTransaction):
        s3_function: S3Function = await tx.get(S3Function, id)
        if s3_function:
            lambda_id = f"lambda_{id}"
            await self.storage_notification.remove_notification(lambda_id, s3_function.bucket)

