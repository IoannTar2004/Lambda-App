from dataclasses import dataclass


@dataclass
class CreateFunctionCommand:

    name: str
    project_id: int
    environment: str
    function_path: str
    function_name: str
    memory_size: int
    timeout: int
