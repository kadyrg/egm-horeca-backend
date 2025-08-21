from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SqlEnum, DateTime
from enum import Enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from .base import Base
from .user_product_likes import user_product_likes

if TYPE_CHECKING:
    from .cart import Cart
    from .products import Product


class UserRole(str, Enum):
    admin = "admin"
    customer = "customer"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole), default=UserRole.customer, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    cart: Mapped["Cart"] = relationship("Cart", back_populates="user")
    liked_products: Mapped[List["Product"]] = relationship(
        secondary=user_product_likes, back_populates="liked_users"
    )
