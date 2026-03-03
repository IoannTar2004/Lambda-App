from pathlib import Path
import os

from pydantic_settings import BaseSettings


class S3Settings(BaseSettings):
    storage_url: str
    storage_access_key: str
    storage_secret_key: str
    max_file_size_mb: str
    s3_user_files_bucket: str

    class Config:
        env_file = Path(__file__).parent.parent / os.getenv("ENV_FILE", ".env")


s3_settings = S3Settings()
