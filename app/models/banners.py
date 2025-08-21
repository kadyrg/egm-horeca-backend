from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Banner(Base):
    __tablename__ = "banners"

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str] = mapped_column(nullable=False)
