from pathlib import Path
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    KAFKA_BOOTSTRAP_SERVERS: str
    CODE_ARCHIVES_DIRECTORY: str
    CODE_ARCHIVES_CLEAN_INTERVAL_SECONDS: int

    CONSUL_HOST: str
    CONSUL_PORT: int
    ACCESS_HOST: str
    ACCESS_PORT: int
    SERVICE_NAME: str

    class Config:
        env_file = Path(__file__).parent.parent / os.getenv("ENV_FILE", ".env")


settings = Settings()

