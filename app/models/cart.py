from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING, List

from .base import Base

if TYPE_CHECKING:
    from .users import User
    from .products import Product


class Cart(Base):
    __tablename__ = 'carts'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True, nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="cart")
    cart_items: Mapped[List["CartItem"]] = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = 'cart_items'

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey('carts.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)

    cart: Mapped["Cart"] = relationship("Cart", back_populates="cart_items")
    product: Mapped["Product"] = relationship("Product", back_populates="cart_items")
