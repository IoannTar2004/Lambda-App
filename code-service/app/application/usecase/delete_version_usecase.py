from application.ports.storage import Storage
from application.usecase.commands.zip_project_command import ZipProjectCommand
from settings import settings


class DeleteVersionUsecase:

    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, data: ZipProjectCommand):
        await self.storage.delete(settings.S3_CODE_ARCHIVES_BUCKET, [f"{data.user_id}/{data.project_id}"
                                                                   f"/{data.revision_id}.zip"])