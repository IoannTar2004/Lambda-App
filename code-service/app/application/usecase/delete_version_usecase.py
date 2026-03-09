from application.ports.storage import Storage
from application.usecase.commands.delete_version_command import DeleteVersionCommand
from application.usecase.commands.zip_project_command import ZipProjectCommand
from settings import settings


class DeleteVersionUsecase:

    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, data: DeleteVersionCommand):
        await self.storage.delete(settings.S3_CODE_ARCHIVES_BUCKET, f"{data.user_id}/{data.function_name}"
                                                                   f"/v{data.version_number}.zip")