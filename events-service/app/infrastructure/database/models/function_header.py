from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from infrastructure.database.base import Base


class FunctionHeaderModel(Base):

    __tablename__ = "function_headers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    project_name: Mapped[str] = mapped_column(nullable=False)
    current_version_number: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
