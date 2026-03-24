from dataclasses import dataclass


@dataclass
class DeleteVersionCommand:
    user_id: int
    project_id: int
    version_number: int