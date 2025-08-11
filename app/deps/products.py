from decimal import Decimal
from typing import Annotated, List
from fastapi import Form, UploadFile, File, Depends
from slugify import slugify



class ExtraImageCreate:
    def __init__(
            self,
            extra_image: Annotated[UploadFile, File(alias="extraImage")],
            order: Annotated[int, Form(ge=1)],
    ):
        self.extra_image = extra_image
        self.order = order


class ProductCreate:
    def __init__(
            self,
            name_en: Annotated[str, Form(..., min_length=2, max_length=50, alias="nameEn")],
            name_ro: Annotated[str, Form(..., min_length=2, max_length=50, alias="nameRo")],
            description_en: Annotated[str, Form(..., min_length=2, max_length=50, alias="descriptionEn")],
            description_ro: Annotated[str, Form(..., min_length=2, max_length=50, alias="descriptionRo")],
            category_id: Annotated[int, Form(..., ge=1, alias="categoryId")],
            price: Annotated[Decimal, Form()],
            image: Annotated[UploadFile, File(...)],
            extra_image: Annotated[List[UploadFile] | None, File(alias="extraImage")] = None,
            extra_image_order: Annotated[List[int] | None, Form(alias='extraImageOrder')] = None,
            stock: Annotated[int | None, Form(..., ge=1)] = None,
            status: Annotated[bool | None, Form(ge=1)] = None,
    ):
        self.name_en = name_en
        self.name_ro = name_ro
        self.description_en = description_en
        self.description_ro = description_ro
        self.category_id = category_id
        self.price = price
        self.image = image
        self.extra_images = []
        if len(extra_image) != len(extra_image_order):
            raise ValueError("Mismatch between number of extra images and orders")
        for file, order in zip(extra_image, extra_image_order):
            self.extra_images.append(ExtraImageCreate(file, order))
        self.stock = stock
        self.status = status

        self.slug_en = slugify(name_en)
        self.slug_ro = slugify(name_ro)

def slugify_for_update(text: str | None) -> str | None:
    if not text:
        return None
    return slugify(text)


class ExtraImageUpdate:
    def __init__(
            self,
            extra_image: Annotated[UploadFile, File(alias="extraImage")],
            order: Annotated[int, Form(ge=1)],
    ):
        self.extra_image = extra_image
        self.order = order


class ProductUpdate:
    def __init__(
            self,
            name_en: Annotated[str | None, Form(min_length=2, max_length=50, alias="nameEn")] = None,
            name_ro: Annotated[str | None, Form(..., min_length=2, max_length=50, alias="nameRo")] = None,
            description_en: Annotated[str | None, Form(..., min_length=2, max_length=50, alias="descriptionEn")] = None,
            description_ro: Annotated[str | None, Form(..., min_length=2, max_length=50, alias="descriptionRo")] = None,
            category_id: Annotated[int | None, Form(..., ge=1, alias="categoryId")] = None,
            price: Annotated[Decimal | None, Form()] = None,
            image: Annotated[UploadFile | None, File(...)] = None,
            stock: Annotated[int | None, Form(..., ge=1)] = None,
            status: Annotated[bool | None, Form(ge=1)] = None,
    ):
        self.name_en = name_en
        self.name_ro = name_ro
        self.description_en = description_en
        self.description_ro = description_ro
        self.category_id = category_id
        self.price = price
        self.image = image
        self.stock = stock
        self.status = status
        self.slug_en = slugify_for_update(name_en)
        self.slug_ro = slugify_for_update(name_ro)

    def dict(self, exclude_none=True):
        d = {
            "name_en": self.name_en,
            "name_ro": self.name_ro,
            "description_en": self.description_en,
            "description_ro": self.description_ro,
            "category_id": self.category_id,
            "price": self.price,
            "stock": self.stock,
            "status": self.status,
            "slug_en": self.slug_en,
            "slug_ro": self.slug_ro,
        }
        if exclude_none:
            return {k: v for k, v in d.items() if v is not None}
        return d
