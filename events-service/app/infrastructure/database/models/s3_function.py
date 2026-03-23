from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from infrastructure.database.base import Base


class S3FunctionModel(Base):

    __tablename__ = "s3_functions"

    id: Mapped[int] = mapped_column(BigInteger, ForeignKey("functions.id"), primary_key=True)
    bucket: Mapped[str] = mapped_column(nullable=False)
    events: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    prefix: Mapped[str] = mapped_column(nullable=False)
    suffix: Mapped[str] = mapped_column(nullable=False)

    function: Mapped["FunctionModel"] = relationship()