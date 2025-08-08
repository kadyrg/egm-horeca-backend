import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException

from app.core import settings
from app.models import User


def generate_access_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + (timedelta(minutes=settings.access_token_validity))
    payload = {
        "user_id": user.id,
        "role": user.role,
        "type": "access",
        "exp": expire,
    }
    return jwt.encode(payload, settings.access_token_secret, algorithm=settings.jwt_algorithm)


def generate_refresh_token(user: User) -> str:
    expire = datetime.now(timezone.utc) + (timedelta(minutes=settings.refresh_token_validity))
    payload = {
        "user_id": user.id,
        "role": user.role,
        "type": "refresh",
        "exp": expire,
    }
    return jwt.encode(payload, settings.refresh_token_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.access_token_secret, algorithms=[settings.jwt_algorithm])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("user_id")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired token")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
