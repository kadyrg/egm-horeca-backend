import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from typing import Tuple

from app.core import settings
from app.models import User


def generate_access_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + (timedelta(minutes=settings.access_token_validity))
    payload = {
        'sub': user.id,
        'role': user.role,
        'type': 'access',
        'exp': expire,
    }
    return jwt.encode(payload, settings.access_token_secret, algorithm=settings.jwt_algorithm)


def generate_refresh_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + (timedelta(minutes=settings.refresh_token_validity))
    payload = {
        'sub': user.id,
        'role': user.role,
        'type': 'refresh',
        'exp': expire,
    }
    return jwt.encode(payload, settings.refresh_token_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> Tuple[int, str]:
    try:
        payload = jwt.decode(token, settings.access_token_secret, algorithms=[settings.jwt_algorithm])
        if payload.get('type') != 'access':
            raise HTTPException(status_code=401, detail='Invalid token type')
        user_id = payload.get('sub')
        role = payload.get('role')
        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail='Invalid token payload')
        return user_id, role
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired token')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def decode_refresh_token(token: str) -> Tuple[int, str]:
    try:
        payload = jwt.decode(token, settings.refresh_token_secret, algorithms=[settings.jwt_algorithm])
        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=401, detail='Invalid token type')
        user_id = payload.get('sub')
        role = payload.get('role')
        if user_id is None or role is None:
            raise HTTPException(status_code=401, detail='Invalid token payload')
        return user_id, role
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired token')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')
