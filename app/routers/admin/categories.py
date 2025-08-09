from fastapi import APIRouter, Form, UploadFile, File, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.models import User
from app.schemas import StatusRes
from app.crud import add_category
from app.deps import get_admin_user


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
