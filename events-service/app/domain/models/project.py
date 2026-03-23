from dataclasses import dataclass, field


@dataclass
class Project:

    user_id: int
    project_name: str
    version_number: int

    id: int | None = None
    relations: dict = field(default_factory=dict)
