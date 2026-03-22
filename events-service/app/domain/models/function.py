from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Function:
    user_id: int
    name: str
    project_version: int
    project_id: int
    language: str

    id: int | None = None
    relations : dict = field(default_factory=dict)