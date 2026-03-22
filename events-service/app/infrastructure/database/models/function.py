from enum import Enum

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from infrastructure.database.base import Base


class LanguageEnum(str, Enum):
    PYTHON = "python"

class FunctionModel(Base):

    __tablename__ = "functions"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(nullable=False)
    project_version: Mapped[int] = mapped_column(BigInteger, nullable=False)
    project_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('projects.id'))
    language: Mapped[LanguageEnum]

    function_handlers: Mapped[list["FunctionHandlerModel"]] = relationship(back_populates="function",
                                                                           cascade="all, delete-orphan")
    project: Mapped["ProjectModel"] = relationship(back_populates="functions")