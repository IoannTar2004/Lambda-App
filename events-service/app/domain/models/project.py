from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Project:

    user_id: int
    project_name: str
    version_number: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    id: int | None = None
    relations: dict = field(default_factory=dict)
