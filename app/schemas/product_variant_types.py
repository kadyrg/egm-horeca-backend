from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, List


# Admin


class ProductVariantTypeIn(BaseModel):
    name_en: Annotated[str, Field(alias="nameEn")]
    name_ro: Annotated[str, Field(alias="nameRo")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductVariantTypeListView(ProductVariantTypeIn):
    id: Annotated[int, Field(alias="id")]
    variants_count: Annotated[int, Field(alias="variantsCount")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductVariantTypeListViewAll(BaseModel):
    id: Annotated[int, Field(alias="id")]
    name_en: Annotated[str, Field(alias="nameEn")]
    name_ro: Annotated[str, Field(alias="nameRo")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductVariantTypeListAdmin(BaseModel):
    data: Annotated[List[ProductVariantTypeListView], Field(alias="data")]
    total: Annotated[int, Field(ge=0, alias="total")]
    initial: Annotated[int, Field(ge=0, alias="initial")]
    last: Annotated[int, Field(ge=0, alias="last")]
    total_pages: Annotated[int, Field(ge=0, alias="totalPages")]
    page: Annotated[int, Field(ge=0, alias="page")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


# Client


class ProductVariantTypeDetail(BaseModel):
    name: Annotated[str, Field(alias="name")]
    # variants:
