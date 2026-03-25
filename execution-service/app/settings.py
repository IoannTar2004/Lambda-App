from pathlib import Path
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    KAFKA_BOOTSTRAP_SERVERS: str

    CODE_ARCHIVES_DIRECTORY: str
    CODE_ARCHIVES_CLEAN_INTERVAL_SECONDS: int
    LAMBDA_SCRIPT_PATH: str

    CONSUL_HOST: str
    CONSUL_PORT: int
    ACCESS_HOST: str
    ACCESS_PORT: int
    SERVICE_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = Path(__file__).parent.parent / os.getenv("ENV_FILE", ".env")


settings = Settings()

