from dataclasses import dataclass


@dataclass
class UpdateHandlerCommand:
    function_id: int
    function_path: str
    function_name: str
    memory_size: int
    timeout: int