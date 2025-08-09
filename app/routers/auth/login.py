from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import Login
from app.crud import login


router = APIRouter(prefix='/login', tags=['Login'])

@router.post('')
async def _login(
        login_in: Login,
        res: Response,
        session: AsyncSession = Depends(get_db_session),
):
    return await login(login_in, res, session)

@router.post('/google')
async def google_login():
    pass
