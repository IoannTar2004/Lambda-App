from dataclasses import dataclass


@dataclass
class UpdateProjectCommand:
    id: int
    fu: str
    memory_size: int
    timeout: int