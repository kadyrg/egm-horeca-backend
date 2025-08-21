from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.crud import verify_email
from app.schemas import VerifyEmail


router = APIRouter(prefix="/verify", tags=["Verify"])


@router.post("/email")
async def _verify_email(
    verify_email_in: VerifyEmail, session: AsyncSession = Depends(get_db_session)
):
    return await verify_email(verify_email_in, session)
