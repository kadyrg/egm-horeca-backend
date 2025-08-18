from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db_session
from app.models import User, UserRole
from app.utils import decode_access_token, decode_refresh_token


security = HTTPBearer()

async def check_admin(
        user_id: int,
        session: AsyncSession = Depends(get_db_session)
) -> User:
    stmt = select(User).where(
        User.id == user_id,
        User.role == UserRole.admin,
        User.is_active == True,
        User.is_verified == True
    )
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or not admin")
    return user


async def check_user(
        user_id: int,
        session: AsyncSession
) -> User:
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or not admin")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="User is not active")
    if not user.is_verified:
        raise HTTPException(status_code=401, detail="User is not verified")
    return user


async def get_user(
        request: Request,
        session: AsyncSession = Depends(get_db_session)
) -> User:
    token = request.cookies.get("accessToken")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id, role = decode_access_token(token)
    return await check_user(int(user_id), session)


async def get_admin_user(
        request: Request,
        session: AsyncSession = Depends(get_db_session)
) -> User:
    token = request.cookies.get("accessToken")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id, role = decode_access_token(token)
    if role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return await check_admin(user_id, session)


async def get_refresh_user(
        request: Request,
        session: AsyncSession = Depends(get_db_session)
) -> User:
    refresh_token = request.cookies.get("refreshToken")
    user_id, role = decode_refresh_token(refresh_token)
    return await check_user(int(user_id), session)
