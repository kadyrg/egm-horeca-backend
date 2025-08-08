from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from .schemas import Register, RegisterResponse
from . import crud


router = APIRouter(
    prefix="/register",
    tags=["Register"]
)

@router.post(
    path="",
    summary="Register",
    description="Register",
    response_model=RegisterResponse
)
async def register(
        register_in: Register,
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.register(register_in, session)
