from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Annotated

from app.db import get_db_session
from . import crud
from app.dependencies import language_dependency
from app.schemas import Category, CategoryDetail
from app.schemas import Products


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.get(
    path="",
    summary="Get Categories",
    description="Get Categories",
    response_model=List[Category]
)
async def get_categories(
        language: str = Depends(language_dependency),
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_categories(language, session)


@router.get(
    path="/{slug}",
    summary="Get Category",
    description="Get Category",
    response_model=CategoryDetail
)
async def get_category(
        slug: str,
        language: str = Depends(language_dependency),
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_category(slug, language, session)


@router.get(
    path="/{slug}/products",
    summary="Get Category Products",
    description="Get Category Products",
    response_model=Products
)
async def get_category_products(
        slug: str,
        language: str = Depends(language_dependency),
        page: Annotated[int, Query(..., ge=1)] = 1,
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_category_products(slug, language, page, session)
