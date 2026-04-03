from dataclasses import dataclass


@dataclass
class ZipProjectCommand:
    user_id: int
    project_id: int
    revision_id: int
