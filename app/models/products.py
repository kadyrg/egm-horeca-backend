from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Numeric
from typing import TYPE_CHECKING
from decimal import Decimal

from .base import Base

if TYPE_CHECKING:
    from .categories import Category


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(unique=True, nullable=False)
    name_ro: Mapped[str] = mapped_column(unique=True, nullable=False)
    description_en: Mapped[str] = mapped_column(nullable=False)
    description_ro: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    image: Mapped[str] = mapped_column(nullable=False)
    slug_en: Mapped[str] = mapped_column(unique=True, nullable=False)
    slug_ro: Mapped[str] = mapped_column(unique=True, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    stock: Mapped[int] = mapped_column(default=0, nullable=False)
    status: Mapped[bool] = mapped_column(default=True, nullable=True)
