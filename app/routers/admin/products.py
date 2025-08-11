from typing import List, Annotated
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import get_db_session
from app.crud import get_products_admin, add_product, update_product, get_product_admin
from app.deps import ProductCreate, ProductUpdate
from app.schemas import ProductListAdmin, StatusRes, ProductDetailAdmin


router = APIRouter(prefix='/products', tags=['Products'])

@router.get('', response_model=List[ProductListAdmin])
async def _get_products_admin(session: AsyncSession = Depends(get_db_session)):
    return await get_products_admin(session)


@router.post('', response_model=StatusRes)
async def _add_product(
        product_in: Annotated[ProductCreate, Depends(ProductCreate)],
        session: AsyncSession = Depends(get_db_session)
):
    return await add_product(product_in, session)


@router.post('/{product_id}', response_model=ProductDetailAdmin)
async def _get_product_admin(
        product_id: Annotated[int, Path(..., ge=1)],
        session: AsyncSession = Depends(get_db_session)
):
    return await get_product_admin(product_id, session)



@router.patch('/{product_id}', response_model=StatusRes)
async def _update_product(
        product_id: Annotated[int, Path(..., ge=1)],
        product_in: Annotated[ProductUpdate, Depends(ProductUpdate)],
        session: AsyncSession = Depends(get_db_session)
):
    return await update_product(product_id, product_in, session)
