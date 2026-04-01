from datetime import datetime, timezone

from sqlalchemy import BigInteger, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class ExecutionLogModel(Base):

    __tablename__ = "execution_logs"

    id: Mapped[str] = mapped_column(primary_key=True)
    function_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('functions.id'))
    execution_time: Mapped[float] = mapped_column(nullable=False)
    created_at = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    function: Mapped["FunctionModel"] = relationship(back_populates="logs")