from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum
from sqlalchemy import Enum as SqlEnum

from .base import Base


class ConfType(str, Enum):
    new_products_count = "new_products_count"
    page_size = "page_size"


class Conf(Base):
    __tablename__ = "conf"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[ConfType] = mapped_column(SqlEnum(ConfType), unique=True, nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
