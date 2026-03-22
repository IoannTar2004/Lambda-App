from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FunctionHandler:

    function_id: int
    project_version: int
    function_path: str
    function_name: str
    memory_size: int
    timeout: int

    id: int | None = None
    relations : dict = field(default_factory=dict)
