from dataclasses import dataclass


@dataclass
class CreateFunctionCommand:

    name: str
    project_id: int
    environment: str
    handler_path: str
    handler: str
    memory_size: int
    timeout: int
