from dataclasses import field, dataclass

@dataclass
class ProjectRevision:

    __tablename__ = "project_revisions"

    project_id: int
    version_number: int

    id: int | None = None
    relations : dict = field(default_factory=dict)

