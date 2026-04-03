from dataclasses import dataclass


@dataclass
class UpdateHandlerCommand:
    function_id: int
    handler_path: str
    handler: str
    memory_size: int
    timeout: int