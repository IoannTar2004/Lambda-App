from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Function:
    user_id: int
    name: str
    service: str
    project_version: int
    base_version: int
    project_id: int
    environment: str

    created_at: datetime = field(default_factory=datetime.now)
    id: int | None = None
    relations : dict = field(default_factory=dict)