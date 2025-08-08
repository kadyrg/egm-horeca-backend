from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum
from sqlalchemy import Enum as SqlEnum, JSON

from .base import Base


class MetaDataGroup(str, Enum):
    messages_en = "messages_en"
    homepage = "homepage"
    product_page = "product_page"
    register_page = "register_page"
    verify_email_page = "verify_email_page"
    website = "website"


class MetaData(Base):
    __tablename__ = "metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MetaDataGroup] = mapped_column(SqlEnum(MetaDataGroup), unique=True, nullable=False)
    value: Mapped[dict] = mapped_column(JSON, nullable=False)
