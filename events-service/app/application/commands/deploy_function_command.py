from dataclasses import dataclass


@dataclass
class DeployFunctionCommand:
    function_name: str
    handler: str
    memory_size: int
    timeout: int