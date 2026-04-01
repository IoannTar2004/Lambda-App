from pathlib import Path
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    S3_CODE_URL: str
    S3_CODE_ACCESS_KEY: str
    S3_CODE_SECRET_KEY: str
    MAX_FILE_SIZE_MB: str
    S3_USER_CODE_BUCKET: str
    S3_CODE_ARCHIVES_BUCKET: str
    S3_FUNCTION_LOGS_BUCKET: str

    CONSUL_HOST: str
    CONSUL_PORT: str
    ACCESS_HOST: str
    ACCESS_PORT: str
    SERVICE_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    USER_CODE_ARCHIVE_PATH: str

    JWT_SECRET_KEY:str
    JWT_SECRET_ALGORITHM: str
    JWT_SECRET_EXPIRES_SECONDS: int

    COMMUNICATION_TOKEN: str

    class Config:
        env_file = Path(__file__).parent.parent / os.getenv("ENV_FILE", ".env")


settings = Settings()

