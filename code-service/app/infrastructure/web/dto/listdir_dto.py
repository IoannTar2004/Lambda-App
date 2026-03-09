from datetime import datetime
from typing import Any

from pydantic import BaseModel


class ListdirDto(BaseModel):
    directories: list[str]
    files: list[dict[str, Any]]