from application.usecase.save_code_usecase import SaveCodeUseCase
from settings import settings
from infrastructure.storage.minio_service import MinioService

save_code_usecase = SaveCodeUseCase(MinioService(settings.storage_url,
                                                     settings.storage_access_key,
                                                     settings.storage_secret_key,
                                                     False))
