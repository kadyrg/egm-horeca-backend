from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db import get_db_session
from app.schemas import StatusRes, ProductVariantIn, ProductVariantListView
from app.crud import add_product_variant, get_product_variants_all


router = APIRouter(prefix="/product_variants", tags=["Product Variants"])


@router.post("", response_model=StatusRes)
async def _add_product_variant(
    product_variant_in: ProductVariantIn,

    session: AsyncSession = Depends(get_db_session),
):
    return await add_product_variant(product_variant_in, session)


@router.get("/all", response_model=List[ProductVariantListView])
async def _get_product_variants_all(
    session: AsyncSession = Depends(get_db_session),
):
    return await get_product_variants_all(session)
