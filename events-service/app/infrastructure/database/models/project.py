from sqlalchemy import BigInteger, func, DateTime, text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from infrastructure.database.base import Base


class ProjectModel(Base):

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    project_name: Mapped[str] = mapped_column(nullable=False)
    version_number: Mapped[int] = mapped_column(nullable=False)
    created_at = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    functions: Mapped[list["FunctionModel"]] = relationship(back_populates="project",
                                                                   cascade="all, delete-orphan")

    last_revision: Mapped["ProjectRevisionModel"] = (
        relationship(back_populates="project",
                     cascade="all, delete-orphan",
                     primaryjoin="""and_(
                                        ProjectModel.id == ProjectRevisionModel.project_id,
                                        ProjectModel.version_number == ProjectRevisionModel.version_number
                                    )"""))