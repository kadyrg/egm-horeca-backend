from typing import List, Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import get_db_session
from app.crud import get_products_admin, get_product
from app.schemas import ProductListAdmin, ProductDetailAll
from app.deps import lang_dep


router = APIRouter(prefix='/products', tags=['Products'])

@router.get('', response_model=List[ProductListAdmin])
async def _get_products_admin(session: AsyncSession = Depends(get_db_session)):
    return await get_products_admin(session)
