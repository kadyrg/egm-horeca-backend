from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, Numeric
from typing import TYPE_CHECKING, List
from decimal import Decimal

from .base import Base
from .user_product_likes import user_product_likes

if TYPE_CHECKING:
    from .categories import Category
    from .cart import CartItem
    from .users import User


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(unique=True, nullable=False)
    name_ro: Mapped[str] = mapped_column(unique=True, nullable=False)
    description_en: Mapped[str] = mapped_column(nullable=False)
    description_ro: Mapped[str] = mapped_column(nullable=False)
    slug_en: Mapped[str] = mapped_column(unique=True, nullable=False)
    slug_ro: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_top: Mapped[bool] = mapped_column(default=False, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    stock: Mapped[int] = mapped_column(default=0, nullable=True)
    main_image: Mapped[str] = mapped_column(nullable=False)
    extra_image_1: Mapped[str] = mapped_column(nullable=True)
    extra_image_2: Mapped[str] = mapped_column(nullable=True)
    extra_image_3: Mapped[str] = mapped_column(nullable=True)
    extra_image_4: Mapped[str] = mapped_column(nullable=True)
    extra_image_5: Mapped[str] = mapped_column(nullable=True)
    extra_image_6: Mapped[str] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    status: Mapped[bool] = mapped_column(default=True, nullable=False)
    cart_items: Mapped[List["CartItem"]] = relationship(
        "CartItem",
        back_populates="product",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    liked_users: Mapped[List["User"]] = relationship(
        secondary=user_product_likes, back_populates="liked_products"
    )
    variants: Mapped[List["ProductVariant"]] = relationship(
        "ProductVariant", back_populates="product"
    )
    specifications: Mapped[List["ProductSpecification"]] = relationship(
        "ProductSpecification", back_populates="product"
    )


class ProductSpecificationType(Base):
    __tablename__ = "product_specification_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(unique=True, nullable=False)
    name_ro: Mapped[str] = mapped_column(unique=True, nullable=False)
    product_specifications: Mapped[List["ProductSpecification"]] = relationship(
        "ProductSpecification", back_populates="specification_type"
    )


class ProductSpecification(Base):
    __tablename__ = "product_specifications"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(nullable=False)
    name_ro: Mapped[str] = mapped_column(nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    product: Mapped["Product"] = relationship(
        "Product", back_populates="specifications"
    )
    specification_type_id: Mapped[int] = mapped_column(
        ForeignKey("product_specification_types.id"), nullable=False
    )
    specification_type: Mapped["ProductSpecificationType"] = relationship(
        "ProductSpecificationType", back_populates="product_specifications"
    )


class ProductVariantType(Base):
    __tablename__ = "product_variant_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(unique=True, nullable=False)
    name_ro: Mapped[str] = mapped_column(unique=True, nullable=False)
    variants: Mapped[List["ProductVariant"]] = relationship(
        "ProductVariant", back_populates="variant_type"
    )


class ProductVariant(Base):
    __tablename__ = "product_variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_en: Mapped[str] = mapped_column(nullable=False)
    name_ro: Mapped[str] = mapped_column(nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    product: Mapped["Product"] = relationship("Product", back_populates="variants")
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=True)
    stock: Mapped[int] = mapped_column(default=0, nullable=True)
    variant_type_id: Mapped[int] = mapped_column(
        ForeignKey("product_variant_types.id"), nullable=False
    )
    variant_type: Mapped["ProductVariantType"] = relationship(
        "ProductVariantType", back_populates="variants"
    )
