from fastapi import APIRouter, Form, UploadFile, File, Depends
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import StatusRes, CategoryAdminList
from app.crud import add_category, get_categories_admin, update_category


router = APIRouter(prefix='/categories', tags=['Categories'])

@router.post("", response_model=StatusRes)
async def _add_category(
        name_en: Annotated[str, Form(..., alias="nameEn", min_length=2, max_length=50)],
        name_ro: Annotated[str, Form(..., alias="nameRo", min_length=2, max_length=50)],
        image: Annotated[UploadFile, File(..., alias="image")],
        session: AsyncSession = Depends(get_db_session),
):
    return await add_category(name_en, name_ro, image, session)

@router.get("", response_model=List[CategoryAdminList])
async def _get_categories_admin(
        session: AsyncSession = Depends(get_db_session),
):
    return await get_categories_admin(session)

@router.patch("/{category_id}", response_model=StatusRes)
async def _update_category(
        category_id: int,
        name_en: Annotated[str | None, Form(alias="nameEn", min_length=2, max_length=50)] = None,
        name_ro: Annotated[str | None, Form(alias="nameRo", min_length=2, max_length=50)] = None,
        image: Annotated[UploadFile | None, File(alias="image")] = None,
        session: AsyncSession = Depends(get_db_session),
):
    return await update_category(category_id, name_en, name_ro, image, session)
