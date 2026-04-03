from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class ProjectRevisionModel(Base):

    __tablename__ = "project_revisions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id'))
    version_number: Mapped[int] = mapped_column(nullable=False)

    project: Mapped["ProjectModel"] = relationship(back_populates="last_revision")

