from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, List


# Client


class CategoryList(BaseModel):
    id: int
    name: str
    slug: str


# Admin


class CategoryIn(BaseModel):
    name_en: Annotated[str, Field(..., min_length=1, max_length=50, alias="nameEn")]
    name_ro: Annotated[str, Field(..., min_length=1, max_length=50, alias="nameRo")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class CategoryInResponse(CategoryIn):
    name_en: Annotated[str, Field(alias="nameEn")]
    name_ro: Annotated[str, Field(alias="nameRo")]
    image: Annotated[str, Field(alias="image")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class CategoryListView(CategoryIn):
    id: int
    image: str
    product_count: Annotated[int, Field(alias="productCount")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class CategoryListViewAll(CategoryIn):
    id: int
    image: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class CategoryListAdmin(BaseModel):
    data: Annotated[List[CategoryListView], Field(..., alias="data")]
    total: Annotated[int, Field(ge=0, alias="total")]
    initial: Annotated[int, Field(ge=0, alias="initial")]
    last: Annotated[int, Field(ge=0, alias="last")]
    total_pages: Annotated[int, Field(ge=0, alias="totalPages")]
    page: Annotated[int, Field(ge=0, alias="page")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


# Above don't touch


class CategoryDetail(BaseModel):
    id: int
    name: str
    slug: str
    image: str
    total_products: Annotated[int, Field(..., alias="totalProducts")]
    total_pages: Annotated[int, Field(..., alias="totalPages")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
