import io
import zipfile

from fastapi import HTTPException

from application.ports.storage import Storage
from application.usecase.commands.zip_project_command import ZipProjectCommand
from settings import settings


class ZipProjectUsecase:

    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, data: ZipProjectCommand):
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            files = await self.storage.recursive_listdir(settings.S3_USER_CODE_BUCKET,
                                                         f"{data.user_id}/{data.project_id}")
            if not files:
                raise HTTPException(status_code=404, detail="Prefix is not found")

            for file_info in files:
                stream = self.storage.download(settings.S3_USER_CODE_BUCKET, file_info["Key"])

                file_buffer = io.BytesIO()
                async for chunk in stream:
                    file_buffer.write(chunk)

                file_buffer.seek(0)
                zip_key = file_info["Key"].split("/", 2)[-1]
                zip_file.writestr(zip_key, file_buffer.read())

            zip_buffer.seek(0)

        await self.storage.upload(settings.S3_CODE_ARCHIVES_BUCKET,
                                  f"300904/{data.project_id}/{data.revision_id}.zip",
                                  zip_buffer.getvalue())


