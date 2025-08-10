from decimal import Decimal
from email.mime import image
from typing import Annotated, List
from fastapi import Form, UploadFile, File, Depends
from slugify import slugify



class ExtraImageCreate:
    def __init__(
            self,
            extra_image: Annotated[UploadFile, File()],
            order: Annotated[int, Form(ge=1)],
    ):
        self.extra_image = extra_image
        self.order = order


class ProductCreate:
    def __init__(
            self,
            name_en: Annotated[str, Form(..., min_length=2, max_length=50)],
            name_ro: Annotated[str, Form(..., min_length=2, max_length=50)],
            description_en: Annotated[str, Form(..., min_length=2, max_length=50)],
            description_ro: Annotated[str, Form(..., min_length=2, max_length=50)],
            category_id: Annotated[int, Form(..., ge=1)],
            price: Annotated[Decimal, Form(..., min_length=2, max_length=50)],
            image: Annotated[UploadFile, File(...)],
            extra_images: Annotated[List[ExtraImageCreate] | None, Depends()] = None,
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
        self.extra_images = extra_images
        self.stock = stock
        self.status = status

        self.slug_en = slugify(name_en)
        self.slug_ro = slugify(name_ro)
