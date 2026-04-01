from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ExecutionLog:

    id: str
    function_id: int
    execution_time: float

    created_at: datetime = field(default_factory=datetime.now)
