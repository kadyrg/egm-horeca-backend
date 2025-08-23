from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends, Query, Path
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import get_db_session
from app.schemas import BannerListAdmin, StatusRes
from app.crud import add_banner, get_banners_admin, delete_banner_admin, update_banner_admin


router = APIRouter(prefix="/banners", tags=["Banners"])

@router.post('', response_model=StatusRes)
async def _add_banner(
        image: Annotated[UploadFile, File(...)],
        session: AsyncSession = Depends(get_db_session)
):
    return await add_banner(image, session)


@router.get("", response_model=BannerListAdmin)
async def _get_banners_admin(
        page: Annotated[int, Query(..., alias="page")] = 1,
        session: AsyncSession = Depends(get_db_session),
):
    return await get_banners_admin(page, session)

@router.patch("/{banner_id}", response_model=StatusRes)
async def _update_banner_admin(
        banner_id: Annotated[int, Path(...)],
        image: Annotated[UploadFile, File(...)],
        session: AsyncSession = Depends(get_db_session),
):
    return await update_banner_admin(banner_id, image, session)


@router.delete("/{id}", response_model=StatusRes)
async def _delete_banner_admin(
    id: Annotated[int, Path(...)],
    session: AsyncSession = Depends(get_db_session),
):
    return await delete_banner_admin(id, session)

