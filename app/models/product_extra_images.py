from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey

from .base import Base

if TYPE_CHECKING:
    from .products import Product


class ProductExtraImages(Base):
    __tablename__ = 'product_extra_images'

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    order: Mapped[int] = mapped_column(nullable=False)
    product: Mapped["Product"] = relationship("Product", back_populates="extra_images")
