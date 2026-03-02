from pathlib import Path
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    frontend_url: str
    storage_url: str
    storage_access_key: str
    storage_secret_key: str
    max_file_size_mb: str
    s3_user_codes_bucket: str

    class Config:
        env_file = Path(__file__).parent.parent / os.getenv("ENV_FILE", ".env")


settings = Settings()
