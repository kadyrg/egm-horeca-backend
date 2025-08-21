from __future__ import annotations
from sqlalchemy import Column, Table, ForeignKey

from .base import Base


user_product_likes = Table(
    "user_product_likes",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "product_id", ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
    ),
)
