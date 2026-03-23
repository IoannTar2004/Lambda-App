from dataclasses import dataclass


@dataclass
class ZipProjectCommand:
    user_id: int
    project_id: int
    project_name: str
    version_number: int