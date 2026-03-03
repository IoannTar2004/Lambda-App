from pathlib import Path
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    S3_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    MAX_FILE_SIZE_MB: str
    S3_USER_FILES_BUCKET: str

    class Config:
        env_file = Path(__file__).parent.parent / os.getenv("ENV_FILE", ".env")


settings = Settings()

