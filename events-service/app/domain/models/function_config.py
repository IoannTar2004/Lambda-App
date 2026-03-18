from dataclasses import dataclass


@dataclass
class FunctionConfig:

    function_id: int
    version_number: int
    handler: str
    memory_size: int
    timeout: int

    id: int | None = None
