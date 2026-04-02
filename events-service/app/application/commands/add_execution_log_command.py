from dataclasses import dataclass


@dataclass
class AddExecutionLogCommand:

    id: str
    function_id: int
    execution_time: float