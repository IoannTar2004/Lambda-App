from application.usecase.save_code_usecase import SaveCodeUseCase
from application.usecase.storage_operations_usecase import UserFilesOperationsUseCase
from s3settings import s3_settings
from infrastructure.storage.async_s3_service import AsyncS3Service

save_code_usecase = SaveCodeUseCase(AsyncS3Service(s3_settings.storage_url,
                                                   s3_settings.storage_access_key,
                                                   s3_settings.storage_secret_key))

storage_operations_usecase = UserFilesOperationsUseCase(AsyncS3Service(s3_settings.storage_url,
                                                                     s3_settings.storage_access_key,
                                                                     s3_settings.storage_secret_key))
