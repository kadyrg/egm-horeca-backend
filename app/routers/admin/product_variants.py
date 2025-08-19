from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import (
    StatusRes,
    ProductVariantIn
)
from app.crud import add_product_variant


router = APIRouter(
    prefix='/product_variants',
    tags=['Product Variants']
)

@router.post('', response_model=StatusRes)
async def _add_product_variant(
        product_variant_in: ProductVariantIn,
        session: AsyncSession = Depends(get_db_session)
):
    return await add_product_variant(product_variant_in, session)