from application.usecase.save_code_usecase import SaveCodeUseCase
from application.usecase.user_files_operations_usecase import UserFilesOperationsUseCase
from settings import settings
from infrastructure.storage.async_s3_service import AsyncS3Service

save_code_usecase = SaveCodeUseCase(AsyncS3Service(settings.S3_URL,
                                                   settings.S3_ACCESS_KEY,
                                                   settings.S3_SECRET_KEY))

user_files_operations_usecase = UserFilesOperationsUseCase(AsyncS3Service(settings.S3_URL,
                                                                          settings.S3_ACCESS_KEY,
                                                                          settings.S3_SECRET_KEY))
