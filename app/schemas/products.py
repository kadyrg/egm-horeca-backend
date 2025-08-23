from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, List
from decimal import Decimal

from .categories import CategoryList
from .product_variant_types import ProductVariantTypeDetail


# Admin

class ProductInstanceListView(BaseModel):
    id: int
    products_count: Annotated[int, Field(ge=0, alias="productsCount")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductInstanceListAdmin(BaseModel):
    data: List[ProductInstanceListView]
    total: int
    initial: int
    last: int
    total_pages: Annotated[int, Field(..., alias="totalPages")]
    page: int

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductListView(BaseModel):
    id: int
    name_en: Annotated[str, Field(..., alias="nameEn")]
    name_ro: Annotated[str, Field(..., alias="nameRo")]
    description_en: Annotated[str, Field(..., alias="descriptionEn")]
    description_ro: Annotated[str, Field(..., alias="descriptionRo")]
    category_id: Annotated[int, Field(..., alias="categoryId")]
    price: Decimal
    stock: int
    status: bool
    is_top: Annotated[bool, Field(..., alias="isTop")]
    main_image: Annotated[str | None, Field(alias="mainImage")]
    extra_image_1: Annotated[str | None, Field(alias="extraImage1")]
    extra_image_2: Annotated[str | None, Field(alias="extraImage2")]
    extra_image_3: Annotated[str | None, Field(alias="extraImage3")]
    extra_image_4: Annotated[str | None, Field(alias="extraImage4")]
    extra_image_5: Annotated[str | None, Field(alias="extraImage5")]
    extra_image_6: Annotated[str | None, Field(alias="extraImage6")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductListAdmin(BaseModel):
    data: List[ProductListView]
    total: int
    initial: int
    last: int
    total_pages: Annotated[int, Field(..., alias="totalPages")]
    page: int

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductIn(BaseModel):
    name_en: Annotated[str, Field(..., min_length=1, max_length=50, alias="nameEn")]
    name_ro: Annotated[str, Field(..., min_length=1, max_length=50, alias="nameRo")]
    description_en: Annotated[str, Field(..., alias="descriptionEn")]
    description_ro: Annotated[str, Field(alias="descriptionRo")]
    price: Annotated[Decimal, Field(alias="price")]
    stock: Annotated[int, Field(alias="stock")]
    status: Annotated[bool, Field(alias="status")]
    is_top: Annotated[bool, Field(alias="isTop")]
    category_id: Annotated[int, Field(alias="categoryId")]
    variant_id: Annotated[int, Field(alias="variantId")]
    instance_id: Annotated[int, Field(alias="instanceId")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


# Client


class ProductList(BaseModel):
    id: int
    name: str
    description: str
    main_image: Annotated[str, Field(alias="mainImage")]
    slug: str
    price: Decimal

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductsForSearch(BaseModel):
    id: Annotated[int, Field(alias="id")]
    name_en: Annotated[str, Field(..., alias="nameEn")]
    name_ro: Annotated[str, Field(..., alias="nameRo")]
    description_en: Annotated[str, Field(..., alias="descriptionEn")]
    description_ro: Annotated[str, Field(alias="descriptionRo")]
    price: Annotated[Decimal, Field(alias="price")]
    slug_en: Annotated[str, Field(alias="slugEn")]
    slug_ro: Annotated[str, Field(alias="slugRo")]
    main_image: Annotated[str, Field(alias="mainImage")]
    created_at: Annotated[datetime, Field(alias="createdAt")]
    category_id: Annotated[int, Field(alias="categoryId")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductVariantTypeSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductVariantSchema(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class VariantProduct(BaseModel):
    variant_name: Annotated[str, Field(alias="variantName")]
    slug: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class Variant(BaseModel):
    variant_type_name: Annotated[str, Field(alias="variantTypeName")]
    products: List[VariantProduct]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductDetail(BaseModel):
    id: int
    name: str
    description: str
    price: Decimal
    category: CategoryList
    images: List[str]
    variants: List[Variant]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
