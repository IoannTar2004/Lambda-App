from dataclasses import dataclass


@dataclass
class DeleteFunctionsCommand:
    user_id: int
    function_name: str