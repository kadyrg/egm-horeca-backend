from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import Login, TokenResponse
from app.crud import login


router = APIRouter(prefix='/login', tags=['Login'])

@router.post('', response_model=TokenResponse)
async def _login(
        login_in: Login,
        session: AsyncSession = Depends(get_db_session),
):
    return await login(login_in, session)
