from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING, List

from .base import Base

if TYPE_CHECKING:
    from .products import Product


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(unique=True, nullable=False)
    name_ro: Mapped[str] = mapped_column(unique=True, nullable=False)
    slug_en: Mapped[str] = mapped_column(unique=True, nullable=False)
    slug_ro: Mapped[str] = mapped_column(unique=True, nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)
    products: Mapped[List["Product"]] = relationship(
        "Product", back_populates="category"
    )
