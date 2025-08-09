from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated


class CategoryAdminList(BaseModel):
    id: int
    name_en: str
    name_ro: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class CategoryList(BaseModel):
    id: int
    name: str
    slug: str


class CategoryDetail(BaseModel):
    id: int
    name: str
    slug: str
    image: str
    total_products: Annotated[int, Field(..., alias='totalProducts')]
    total_pages: Annotated[int, Field(..., alias='totalPages')]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
