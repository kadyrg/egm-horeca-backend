from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db import get_db_session
from app.schemas import Login, StatusRes, RegisterResponse, Register
from app.crud import login, refresh, register, verify_email
from app.models import User
from app.deps import refresh_admin_user


router = APIRouter(prefix='/auth')

@router.post(
    '/register',
    tags=['Client: Auth'],
    response_model=RegisterResponse
)
async def _register(
        register_in: Register,
        session: AsyncSession = Depends(get_db_session)
):
    return await register(register_in, session)


@router.get('/email', tags=['Client: Auth'])
async def _verify_email(
        token: Annotated[str, Query(...)],
        res: Response,
        session: AsyncSession = Depends(get_db_session)
):
    return await verify_email(token, res, session)


@router.post(
    '/login',
    tags=['Client: Auth', 'Admin: Auth']
)
async def _login(
        login_in: Login,
        res: Response,
        session: AsyncSession = Depends(get_db_session),
):
    return await login(login_in, res, session)


@router.post(
    '/refresh',
    response_model=StatusRes,
    tags=['Client: Auth', 'Admin: Auth']
)
async def _refresh(
        res: Response,
        user: User = Depends(refresh_admin_user),
        session: AsyncSession = Depends(get_db_session)
):
    return await refresh(res, user, session)
