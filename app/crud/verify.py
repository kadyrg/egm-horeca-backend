from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.schemas import VerifyEmail, TokenResponse
from app.utils import verify_email_token, generate_access_token, generate_refresh_token


async def verify_email(verify_email_in: VerifyEmail, session: AsyncSession):
    email = verify_email_token(verify_email_in.token)
    stmt = select(User).where(User.email==email, User.is_active, User.is_verified==False)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Email not found")
    user.is_verified = True
    await session.commit()
    return TokenResponse(
        access_token=generate_access_token(user),
        refresh_token=generate_refresh_token(user)
    )
