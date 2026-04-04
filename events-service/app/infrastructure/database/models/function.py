from enum import Enum

from sqlalchemy import BigInteger, ForeignKey, func, DateTime
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from infrastructure.database.base import Base


class EnvironmentEnum(str, Enum):
    PYTHON_3 = "Python 3"

class FunctionModel(Base):

    __tablename__ = "functions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(nullable=False)
    service: Mapped[str] = mapped_column(nullable=False)
    project_version: Mapped[int] = mapped_column(nullable=False)
    base_version: Mapped[int] = mapped_column(nullable=False)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id'))
    environment: Mapped[EnvironmentEnum]
    created_at = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    handler: Mapped["FunctionHandlerModel"] = (
        relationship(back_populates="function",
                     cascade="all, delete-orphan",
                     primaryjoin="""and_(
                                    FunctionModel.id == FunctionHandlerModel.function_id,
                                    FunctionModel.project_version == FunctionHandlerModel.project_version
                                )"""))
    project: Mapped["ProjectModel"] = relationship(back_populates="functions")

    logs: Mapped[list["ExecutionLogModel"]] = relationship(back_populates="function")