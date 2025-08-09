from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from app.db import get_db_session
from app.crud import get_categories, get_category, get_category_products
from app.deps import lang_dep
from app.schemas import CategoryList, CategoryDetail, Products


router = APIRouter(prefix='/categories', tags=['Categories'])

@router.get('', response_model=List[CategoryList])
async def _get_categories(
        lang: str = Depends(lang_dep),
        session: AsyncSession = Depends(get_db_session)
):
    return await get_categories(lang, session)


@router.get('/{slug}', response_model=CategoryDetail)
async def _get_category(
        slug: str,
        lang: str = Depends(lang_dep),
        session: AsyncSession = Depends(get_db_session)
):
    return await get_category(slug, lang, session)


@router.get('/{slug}/products', response_model=Products)
async def _get_category_products(
        slug: str,
        lang: str = Depends(lang_dep),
        page: Annotated[int, Query(..., ge=1)] = 1,
        session: AsyncSession = Depends(get_db_session)
):
    return await get_category_products(slug, lang, page, session)
