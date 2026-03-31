from pathlib import Path
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CONSUL_HOST: str
    CONSUL_PORT: str
    ACCESS_HOST: str
    ACCESS_PORT: str
    SERVICE_NAME: str

    S3_USER_URL: str
    S3_USER_ACCESS_KEY: str
    S3_USER_SECRET_KEY: str

    REDIS_HOST: str
    REDIS_PORT: int

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    KAFKA_BOOTSTRAP_SERVERS: str

    JWT_SECRET_KEY: str
    JWT_SECRET_ALGORITHM: str

    COMMUNICATION_TOKEN: str

    class Config:
        env_file = Path(__file__).parent.parent / os.getenv("ENV_FILE", ".env")


settings = Settings()

