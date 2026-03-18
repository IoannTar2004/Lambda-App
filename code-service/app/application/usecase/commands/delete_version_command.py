from dataclasses import dataclass


@dataclass
class DeleteVersionCommand:
    user_id: int
    function_name: str
    version_number: int