from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, HTTPException
from sqlalchemy import select

from app.schemas import StatusRes
from app.schemas.login import Login
from app.models import User
from app.utils import generate_refresh_token, generate_access_token, verify_pwd


async def login(login_in: Login, res: Response, session: AsyncSession) -> StatusRes:
    stmt = select(User).where(User.email == login_in.email, User.is_active, User.is_verified == True)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail='Email not found')
    if not verify_pwd(login_in.password, user.password):
        raise HTTPException(status_code=404, detail='Incorrect password')
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    res.set_cookie(
        key='accessToken',
        value=access_token,
        httponly=True,
        secure=True,
        samesite='lax',
        max_age=60 * 15,
        path='/'
    )
    res.set_cookie(
        key='refreshToken',
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite='lax',
        max_age=60 * 60 * 24 * 30,
        path='/'
    )
    await session.commit()
    return StatusRes(status="success", message="Login successful")
