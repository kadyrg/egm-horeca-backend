from fastapi import APIRouter, Form, UploadFile, File, Depends, Query, Path
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import (
    StatusRes,
    CategoryListAdmin,
    CategoryListView,
    CategoryListViewAll,
    CategoryInResponse,
)
from app.crud import (
    add_category_admin,
    get_categories_admin,
    update_category_admin,
    get_all_categories_admin,
    delete_category_admin,
)


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", response_model=CategoryInResponse)
async def _add_category_admin(
    category_in: Annotated[str, Form(..., alias="categoryIn")],
    image: Annotated[UploadFile, File(..., alias="image")],
    session: AsyncSession = Depends(get_db_session),
):
    return await add_category_admin(category_in, image, session)


@router.get("", response_model=CategoryListAdmin)
async def _get_categories_admin(
    page: Annotated[int, Query(..., alias="page")] = 1,
    session: AsyncSession = Depends(get_db_session),
):
    return await get_categories_admin(page, session)


@router.delete("/{category_id}", response_model=StatusRes)
async def _delete_category_admin(
    category_id: Annotated[int, Path(...)],
    session: AsyncSession = Depends(get_db_session),
):
    return await delete_category_admin(category_id, session)


@router.get("/all", response_model=List[CategoryListViewAll])
async def _get_all_categories_admin(
    session: AsyncSession = Depends(get_db_session),
):
    return await get_all_categories_admin(session)


@router.patch("/{category_id}", response_model=StatusRes)
async def _update_category_admin(
    category_id: Annotated[int, Path(..., ge=1)],
    category_in: Annotated[str, Form(..., alias="categoryIn")],
    image: Annotated[UploadFile | None, File(..., alias="image")] = None,
    session: AsyncSession = Depends(get_db_session),
):
    return await update_category_admin(category_id, category_in, image, session)
