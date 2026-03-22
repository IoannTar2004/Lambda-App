from dataclasses import dataclass


@dataclass
class S3Function:
    bucket: str
    events: list[str]
    prefix: str
    suffix: str

    id: int | None = None