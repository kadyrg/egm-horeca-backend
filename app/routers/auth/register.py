from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.schemas import RegisterResponse, Register
from app.crud import register


router = APIRouter(prefix='/register', tags=['Register'])

@router.post('', response_model=RegisterResponse)
async def _register(
        register_in: Register,
        session: AsyncSession = Depends(get_db_session)
):
    return await register(register_in, session)
