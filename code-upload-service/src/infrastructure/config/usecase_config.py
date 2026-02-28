from application.usecase.upload_code_usecase import UploadCodeUseCase
from settings import settings
from infrastructure.storage.minio_service import MinioService

upload_code_usecase = UploadCodeUseCase(MinioService(settings.storage_url,
                                                     settings.storage_access_key,
                                                     settings.storage_secret_key,
                                                     False))
