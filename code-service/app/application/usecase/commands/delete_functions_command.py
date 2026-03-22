from dataclasses import dataclass


@dataclass
class DeleteArchivesCommand:
    user_id: int
    function_name: str