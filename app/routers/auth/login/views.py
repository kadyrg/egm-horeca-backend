from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from .schemas import Login
from . import crud


router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post(
    path="",
    summary="Login",
    description="Login"
)
async def login(
        login_in: Login,
        response: Response,
        session: AsyncSession = Depends(get_db_session),
):
    return await crud.login(login_in, response, session)

@router.post(
    path="/google",
    summary="Google Login",
    description="Google Login"
)
async def google_login():
    pass
