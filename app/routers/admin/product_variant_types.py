from typing import Annotated, List

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Query
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import (
    ProductVariantTypeListView,
    ProductVariantTypeIn,
    ProductVariantTypeListAdmin, StatusRes
)
from app.crud import (
    add_product_variant_type,
    get_product_variant_types,
    delete_product_variant_type,
    update_product_variant_type,
    get_product_variant_types_all
)


router = APIRouter(
    prefix='/product_variant_types',
    tags=['Product Variant Types']
)

@router.post('', response_model=ProductVariantTypeListView)
async def _add_product_variant_type(
        product_variant_type_in: ProductVariantTypeIn,
        session: AsyncSession = Depends(get_db_session)
):
    return await add_product_variant_type(product_variant_type_in, session)


@router.get('', response_model=ProductVariantTypeListAdmin)
async def _get_product_variant_types(
        page: Annotated[int, Query(ge=1)] = 1,
        session: AsyncSession = Depends(get_db_session)
):
    return await get_product_variant_types(page, session)


@router.get('/all', response_model=List[ProductVariantTypeListView])
async def _get_product_variant_types_all(
        session: AsyncSession = Depends(get_db_session)
):
    return await get_product_variant_types_all(session)



@router.patch('/{product_variant_type_id}', response_model=ProductVariantTypeListView)
async def _update_product_variant_type(
        product_variant_type_id: Annotated[int, Path(ge=1)],
        product_variant_type_in: ProductVariantTypeIn,
        session: AsyncSession = Depends(get_db_session)
):
    return await update_product_variant_type(
        product_variant_type_in,
        product_variant_type_id,
        session
    )


@router.delete('/{product_variant_type_id}', response_model=StatusRes)
async def _delete_product_variant_type(
        product_variant_type_id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(get_db_session)
):
    return await delete_product_variant_type(product_variant_type_id, session)
