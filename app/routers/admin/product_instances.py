from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import get_db_session
from app.schemas import (
    StatusRes,
    ProductInstanceListAdmin, ProductListAdmin
)
from app.crud import (
    add_product_instance,
    delete_product_instance,
    get_products_of_instance_admin,
    get_product_instances_admin
)


router = APIRouter(
    prefix="/product_instances",
    tags=["Product Instances"],
)

@router.post('', response_model=StatusRes)
async def _add_product_instance(
        session: AsyncSession = Depends(get_db_session)
):
    return await add_product_instance(session)


@router.get('', response_model=ProductInstanceListAdmin)
async def _get_product_instances_admin(
        page: Annotated[int, Path(..., ge=1)] = 1,
        session: AsyncSession = Depends(get_db_session),
):
    return await get_product_instances_admin(page, session)


@router.delete('/{product_instance_id}', response_model=StatusRes)
async def _delete_product_instance(
        product_instance_id: Annotated[int, Path(..., ge=1)],
        session: AsyncSession = Depends(get_db_session)
):
    return await delete_product_instance(product_instance_id, session)


@router.get('/{product_instance_id}/products', response_model=ProductListAdmin)
async def _get_products_of_instance_admin(
        product_instance_id: Annotated[int, Path(..., ge=1)],
        page: Annotated[int, Query(ge=1)] = 1,
        session: AsyncSession = Depends(get_db_session)
):
    return await get_products_of_instance_admin(product_instance_id, page, session)
