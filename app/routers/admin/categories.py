from fastapi import APIRouter, Form, UploadFile, File, Depends
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.models import User
from app.schemas import StatusRes, CategoryBase
from app.crud import add_category, get_categories_admin
from app.deps import get_admin_user, lang_dep


router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("", response_model=StatusRes)
async def _add_category(
        name_en: Annotated[str, Form(..., alias="nameEn")],
        name_ro: Annotated[str, Form(..., alias="nameRo")],
        image: Annotated[UploadFile, File(..., alias="image")],
        admin_user: User = Depends(get_admin_user),
        session: AsyncSession = Depends(get_db_session),
):
    return await add_category(name_en, name_ro, image, session)


@router.get("", response_model=List[CategoryBase])
async def _get_categories_admin(
        lang: str = Depends(lang_dep),
        admin_user: User = Depends(get_admin_user),
        session: AsyncSession = Depends(get_db_session),
):
    return await get_categories_admin(lang, session)
