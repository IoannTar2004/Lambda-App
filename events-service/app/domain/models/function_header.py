from dataclasses import dataclass


@dataclass
class FunctionHeader:
    name: str
    project_name: str
    current_version_number: int
    user_id: int
    id: int | None = None

