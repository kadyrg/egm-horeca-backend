from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.deps import refresh_admin_user
from app.crud import refresh
from app.models import User
from app.schemas import StatusRes


router = APIRouter(prefix='/refresh', tags=['Refresh'])

@router.post('', response_model=StatusRes)
async def _refresh(
        res: Response,
        user: User = Depends(refresh_admin_user),
        session: AsyncSession = Depends(get_db_session)
):
    return await refresh(res, user, session)
