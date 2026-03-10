from dataclasses import dataclass


@dataclass
class CreateS3EventCommand:
    function_id: int
    bucket: str
    events: list[str]
    prefix: str
    suffix: str
