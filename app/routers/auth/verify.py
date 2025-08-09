from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db import get_db_session
from app.crud import verify_email


router = APIRouter(prefix='/verify', tags=['Verify'])

@router.get('/email')
async def _verify_email(
        token: Annotated[str, Query(...)],
        res: Response,
        session: AsyncSession = Depends(get_db_session)
):
    return await verify_email(token, res, session)
