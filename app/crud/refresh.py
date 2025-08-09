from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response

from app.models import User
from app.schemas import StatusRes
from app.utils import generate_access_token, generate_refresh_token


async def refresh(res: Response, user: User, session: AsyncSession) -> StatusRes:
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    res.set_cookie(
        key="accessToken",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 15,
        path="/"
    )
    res.set_cookie(
        key="refreshToken",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=60 * 60 * 24 * 30,
        path="/"
    )
    user.is_verified = True
    await session.commit()
    return StatusRes(status="success", message="Successfully refreshed")
