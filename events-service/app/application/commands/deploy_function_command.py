from dataclasses import dataclass


@dataclass
class DeployFunctionCommand:
    id: int
    function_name: str
    project_name: str
    handler: str
    memory_size: int
    timeout: int