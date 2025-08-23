from typing import Annotated, List
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


# Admin


class ProductVariantIn(BaseModel):
    name_en: Annotated[str, Field(..., alias="nameEn")]
    name_ro: Annotated[str, Field(..., alias="nameRo")]
    variant_type_id: Annotated[int, Field(..., alias="productVariantTypeId")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductVariantListView(ProductVariantIn):
    id: Annotated[int, Field(alias="id")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductVariantListViewAll(ProductVariantIn):
    id: Annotated[int, Field(alias="id")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductVariantsListAdmin(BaseModel):
    data: Annotated[List[ProductVariantListView], Field(alias="data")]
    total: Annotated[int, Field(ge=0, alias="total")]
    initial: Annotated[int, Field(ge=0, alias="initial")]
    last: Annotated[int, Field(ge=0, alias="last")]
    total_pages: Annotated[int, Field(ge=0, alias="totalPages")]
    page: Annotated[int, Field(ge=0, alias="page")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


# Client
