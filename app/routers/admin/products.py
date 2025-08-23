from typing import Annotated
from fastapi import APIRouter, Depends, Path, Form, UploadFile, File
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import get_db_session
from app.crud import (
    get_products_admin,
    add_product_admin,
    delete_products_admin,
    update_product_admin,
    get_product_variants_admin,
)
from app.schemas import (
    ProductListAdmin,
    StatusRes,
    ProductVariantsListAdmin,
)


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=ProductListAdmin)
async def _get_products_admin(
    page: Annotated[int, Path(..., ge=1)] = 1,
    session: AsyncSession = Depends(get_db_session),
):
    return await get_products_admin(page, session)


@router.post("", response_model=StatusRes)
async def _add_product_admin(
    product_in: Annotated[str, Form(..., alias="productIn")],
    main_image: Annotated[UploadFile | None, File(..., alias="mainImage")] = None,
    extra_image_1: Annotated[UploadFile | None, File(..., alias="extraImage1")] = None,
    extra_image_2: Annotated[UploadFile | None, File(..., alias="extraImage2")] = None,
    extra_image_3: Annotated[UploadFile | None, File(..., alias="extraImage3")] = None,
    extra_image_4: Annotated[UploadFile | None, File(..., alias="extraImage4")] = None,
    extra_image_5: Annotated[UploadFile | None, File(..., alias="extraImage5")] = None,
    extra_image_6: Annotated[UploadFile | None, File(..., alias="extraImage6")] = None,
    session: AsyncSession = Depends(get_db_session),
):
    return await add_product_admin(
        product_in,
        main_image,
        extra_image_1,
        extra_image_2,
        extra_image_3,
        extra_image_4,
        extra_image_5,
        extra_image_6,
        session,
    )


@router.patch("/{product_id}", response_model=StatusRes)
async def _update_product_admin(
    product_id: Annotated[int, Path(..., ge=1)],
    product_in: Annotated[str, Form(..., alias="productIn")],
    main_image: Annotated[UploadFile | None, File(..., alias="mainImage")] = None,
    extra_image_1: Annotated[UploadFile | None, File(..., alias="extraImage1")] = None,
    extra_image_2: Annotated[UploadFile | None, File(..., alias="extraImage2")] = None,
    extra_image_3: Annotated[UploadFile | None, File(..., alias="extraImage3")] = None,
    extra_image_4: Annotated[UploadFile | None, File(..., alias="extraImage4")] = None,
    extra_image_5: Annotated[UploadFile | None, File(..., alias="extraImage5")] = None,
    extra_image_6: Annotated[UploadFile | None, File(..., alias="extraImage6")] = None,
    session: AsyncSession = Depends(get_db_session),
):
    return await update_product_admin(
        product_id,
        product_in,
        main_image,
        extra_image_1,
        extra_image_2,
        extra_image_3,
        extra_image_4,
        extra_image_5,
        extra_image_6,
        session,
    )


@router.delete("/{product_id}", response_model=StatusRes)
async def _delete_product_admin(
    product_id: Annotated[int, Path(...)],
    session: AsyncSession = Depends(get_db_session),
):
    return await delete_products_admin(product_id, session)


@router.get("/{product_id}/variants", response_model=ProductVariantsListAdmin)
async def _get_product_variants_admin(
    product_id: Annotated[int, Path(...)],
    page: Annotated[int, Path(..., ge=1)] = 1,
    session: AsyncSession = Depends(get_db_session),
):
    return await get_product_variants_admin(page, product_id, session)

