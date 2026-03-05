from pathlib import Path
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CONSUL_HOST: str
    CONSUL_PORT: str
    ACCESS_HOST: str
    ACCESS_PORT: str
    SERVICE_NAME: str

    class Config:
        env_file = Path(__file__).parent.parent / os.getenv("ENV_FILE", ".env")


settings = Settings()

