from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Request
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from app.db import get_db_session
from app.models import User, UserRole
from app.utils import decode_access_token, decode_refresh_token


security = HTTPBearer()



async def check_admin(user_id: int, session: AsyncSession = Depends(get_db_session)) -> User:
    result = await session.execute(select(User).where(User.id == user_id, User.role == UserRole.admin))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found or not admin")
    return user

async def get_admin_user(
        request: Request,
        session: AsyncSession = Depends(get_db_session)
):
    token = request.cookies.get("accessToken")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    user_id, role = decode_access_token(token)
    if role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return await check_admin(user_id, session)


async def refresh_admin_user(
        request: Request,
        session: AsyncSession = Depends(get_db_session)
):
    token = request.cookies.get("refreshToken")
    user_id, role = decode_refresh_token(token)
    if role != UserRole.admin:
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return await check_admin(user_id, session)
