from dataclasses import dataclass


@dataclass
class CreateFunctionCommand:

    function_name: str
    project_name: str
    handler: str
    memory_size: int
    timeout: int
