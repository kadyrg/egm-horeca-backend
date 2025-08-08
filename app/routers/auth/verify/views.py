from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.db import get_db_session
from . import crud


router = APIRouter(
    prefix="/verify",
    tags=["Verify"]
)

@router.get(
    path="/email",
    summary="Verify Email",
    description="Verify Email",
)
async def verify_email(
        token: Annotated[str, Query(...)],
        response: Response,
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.verify_email(token, response, session)
