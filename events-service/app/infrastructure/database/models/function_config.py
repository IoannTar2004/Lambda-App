from sqlalchemy import ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from infrastructure.database.base import Base
from infrastructure.database.models import FunctionHeaderModel


class FunctionConfigModel(Base):

    __tablename__ = "function_configs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    function_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("function_headers.id"))
    version_number: Mapped[int] = mapped_column(nullable=False)
    handler: Mapped[str] = mapped_column(nullable=False)
    memory_size: Mapped[int] = mapped_column(nullable=False)
    timeout: Mapped[int] = mapped_column(nullable=False)

    header: Mapped[FunctionHeaderModel] = relationship(back_populates="config")
    