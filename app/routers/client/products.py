from typing import List, Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import get_db_session
from app.crud import get_products, get_product, get_top_products, get_new_products
from app.schemas import ProductList, ProductDetail, ProductDetailAll
from app.deps import lang_dep


router = APIRouter(prefix='/products', tags=['Products'])

@router.get('', response_model=List[ProductDetailAll])
async def _get_products(
        lang: str = Depends(lang_dep),
        session: AsyncSession = Depends(get_db_session)
):
    return await get_products(lang, session)


@router.get('/top', response_model=List[ProductList])
async def _get_top_products(
        lang: str = Depends(lang_dep),
        session: AsyncSession = Depends(get_db_session)
):
    return await get_top_products(lang, session)


@router.get('/new', response_model=List[ProductList])
async def _get_new_products(
        lang: str = Depends(lang_dep),
        session: AsyncSession = Depends(get_db_session)
):
    return await get_new_products(lang, session)

@router.get('/{slug}', response_model=ProductDetail)
async def _get_product(
        slug: Annotated[str, Path(...)],
        lang: str = Depends(lang_dep),
        session: AsyncSession = Depends(get_db_session)
):
    return await get_product(slug, lang, session)
