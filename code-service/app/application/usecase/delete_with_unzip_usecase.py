import tempfile
import os
import shutil
from pathlib import Path

from application.ports.storage import Storage
from application.usecase.commands.zip_project_command import ZipProjectCommand
from settings import settings


class DeleteWithUnzip:

    def __init__(self, storage: Storage):
        self.storage = storage

    async def execute(self, data: ZipProjectCommand):
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip:
            temp_zip_path = tmp_zip.name

        user_id, project_id, revision_id = data.user_id, data.project_id, data.revision_id

        path = f"{user_id}/{project_id}/{revision_id}.zip"
        try:
            with open(temp_zip_path, 'wb') as f:
                async for chunk in self.storage.download(settings.S3_CODE_ARCHIVES_BUCKET, path):
                    f.write(chunk)

            extract_to = tempfile.mkdtemp()

            shutil.unpack_archive(temp_zip_path, extract_to, 'zip')

            old_listdir = await self.storage.recursive_listdir(settings.S3_USER_CODE_BUCKET, f"{user_id}/{project_id}")
            if old_listdir:
                old_listdir = [key["Key"] for key in old_listdir]
                await self.storage.delete(settings.S3_USER_CODE_BUCKET, old_listdir)

            for file_path in self._get_recursive_listdir(Path(extract_to)):
                key = f"{user_id}/{project_id}/{file_path}"
                with open(os.path.join(extract_to, file_path), 'rb') as f:
                    print(f.name)
                    await self.storage.upload(settings.S3_USER_CODE_BUCKET, key, f.read())

            await self.storage.delete(settings.S3_USER_CODE_BUCKET, [path])

        finally:
            if os.path.exists(temp_zip_path):
                os.unlink(temp_zip_path)


    def _get_recursive_listdir(self, path: Path):
        listdir = []
        for file_path in path.rglob('*'):
            if file_path.is_file():
                relative_path = file_path.relative_to(path).as_posix()
                listdir.append(relative_path)

        return listdir