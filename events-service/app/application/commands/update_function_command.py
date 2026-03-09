from dataclasses import dataclass


@dataclass
class UpdateFunctionCommand:
    id: int
    handler: str
    memory_size: int
    timeout: int