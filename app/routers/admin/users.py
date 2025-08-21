from fastapi import APIRouter, Query, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import UserListAdmin
from app.crud import get_users_admin


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=UserListAdmin)
async def _get_users_admin(
    page: Annotated[int, Query(alias="page")] = 1,
    session: AsyncSession = Depends(get_db_session),
):
    return await get_users_admin(page, session)
