from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.utils import verify_email_token, generate_access_token, generate_refresh_token


async def verify_email(token: str, res: Response, session: AsyncSession):
    email = verify_email_token(token)
    stmt = select(User).where(User.email==email, User.is_active, User.is_verified==False)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Email not found")
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
    return
