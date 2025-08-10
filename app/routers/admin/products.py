from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import get_db_session
from app.crud import get_products_admin, add_product
from app.deps import ProductCreate
from app.schemas import ProductListAdmin, StatusRes

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
