from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request
from typing import List
from app.db import get_db_session
from app.schemas import BannerList
from app.crud import get_banners


router = APIRouter(prefix="/banners", tags=["Banners"])

@router.get("", response_model=List[BannerList])
async def _get_banners(
        request: Request,
        session: AsyncSession = Depends(get_db_session),
):
    return await get_banners(request, session)
