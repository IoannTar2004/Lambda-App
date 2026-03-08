from pathlib import Path
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    S3_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    MAX_FILE_SIZE_MB: str
    S3_USER_FILES_BUCKET: str

    CONSUL_HOST: str
    CONSUL_PORT: str
    ACCESS_HOST: str
    ACCESS_PORT: str
    SERVICE_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = Path(__file__).parent.parent / os.getenv("ENV_FILE", ".env")


settings = Settings()

