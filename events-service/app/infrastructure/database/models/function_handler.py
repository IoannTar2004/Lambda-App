from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class FunctionHandlerModel(Base):

    __tablename__ = "function_handlers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    function_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('functions.id'))
    project_version: Mapped[int] = mapped_column(BigInteger, nullable=False)
    function_path: Mapped[str] = mapped_column(nullable=False)
    function_name: Mapped[str] = mapped_column(nullable=False)
    memory_size: Mapped[int] = mapped_column(nullable=False)
    timeout: Mapped[int] = mapped_column(nullable=False)

    function: Mapped["FunctionModel"] = relationship(back_populates="function_handlers")

