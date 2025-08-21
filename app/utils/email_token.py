from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from fastapi import HTTPException

from app.core import settings


EMAIL_CONFIRM_SALT = "email-confirm-salt"

serializer = URLSafeTimedSerializer(settings.email_confirm_token_secret)


def generate_email_token(email: str) -> str:
    return serializer.dumps(email, salt=EMAIL_CONFIRM_SALT)


def verify_email_token(token: str, max_age: int = settings.email_token_validity) -> str:
    try:
        return serializer.loads(token, salt=EMAIL_CONFIRM_SALT, max_age=max_age)
    except SignatureExpired:
        raise HTTPException(status_code=401, detail="token is expired")
    except BadSignature:
        raise HTTPException(status_code=401, detail="token is invalid")


def create_verification_url(email: str) -> str:
    token = generate_email_token(email)
    return f"{settings.front_end_url}/verify-email?token={token}"
