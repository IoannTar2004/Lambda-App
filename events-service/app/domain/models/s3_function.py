from dataclasses import dataclass, field


@dataclass
class S3Function:
    bucket: str
    events: list[str]
    prefix: str
    suffix: str

    relations: dict = field(default_factory=dict)
    id: int | None = None