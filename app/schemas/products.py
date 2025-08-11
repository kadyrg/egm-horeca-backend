from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, List
from decimal import Decimal
from datetime import datetime

from .categories import CategoryList, CategoryAdminList


class Product(BaseModel):
    name: str
    description: str
    image: str
    slug: str
    price: Decimal


class ProductList(Product):
    id: int



class ProductExtraImageList(BaseModel):
    id: int
    image: str
    order: int

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductDetailAdmin(BaseModel):
    name_en: Annotated[str, Field(alias="nameEn")]
    name_ro: Annotated[str, Field(alias="nameRo")]
    description_en: Annotated[str, Field(alias="descriptionEn")]
    description_ro: Annotated[str, Field(alias="descriptionRo")]
    price: Annotated[Decimal, Field(alias="price")]
    image: Annotated[str, Field(alias="image")]
    category: CategoryAdminList
    stock: int
    status: bool
    extra_images: Annotated[List[ProductExtraImageList], Field(alias="extraImages")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductListAdmin(BaseModel):
    id: int
    name_en: Annotated[str, Field(alias="nameEn")]
    name_ro: Annotated[str, Field(alias="nameRo")]
    price: Decimal
    category: CategoryAdminList
    stock: int
    status: bool

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class ProductCreate(BaseModel):
    name: str
    description: str
    image: str
    slug: str


class ProductDetail(BaseModel):
    id: int
    name: str
    description: str
    image: str
    price: Decimal
    category: CategoryList

class ProductDetailAll(BaseModel):
    id: int
    name_en: Annotated[str, Field(alias="nameEn")]
    name_ro: Annotated[str, Field(alias="nameRo")]
    description_en: Annotated[str, Field(alias="descriptionEn")]
    description_ro: Annotated[str, Field(alias="descriptionRo")]
    price: Annotated[Decimal, Field(alias="price")]
    image: Annotated[str, Field(alias="image")]
    slug_en: Annotated[str, Field(alias="slugEn")]
    slug_ro: Annotated[str, Field(alias="slugRo")]
    category_id: Annotated[int, Field(alias="categoryId")]
    created_at: Annotated[datetime, Field(alias="createdAt")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
