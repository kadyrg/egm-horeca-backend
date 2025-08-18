from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import TokenResponse
from app.crud import refresh
from app.models import User
from app.deps import get_refresh_user


router = APIRouter(prefix='/refresh', tags=['Refresh'])

@router.post('',  response_model=TokenResponse)
async def _refresh(
        user: User = Depends(get_refresh_user),
):
    return await refresh(user)
