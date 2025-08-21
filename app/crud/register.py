from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.register import Register, RegisterResponse
from app.models import User
from app.utils import (
    hash_pwd,
    create_verification_url,
    send_email,
    email_verification_body_text,
    email_verification_body_html,
)


async def register(register_in: Register, session: AsyncSession) -> RegisterResponse:
    stmt = select(User).where(User.email == register_in.email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    if user:
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive")
        if user.is_verified:
            raise HTTPException(status_code=400, detail="User already registered")

        user.email = register_in.email
        user.phone_number = register_in.phone_number
        user.first_name = register_in.first_name
        user.last_name = register_in.last_name
        user.password = hash_pwd(register_in.password)

        verification_url = create_verification_url(register_in.email)

        body_text = email_verification_body_text(verification_url)
        body_html = email_verification_body_html(verification_url)

        send_email(register_in.email, "Verification URL", body_text, body_html)

        await session.commit()
        return RegisterResponse(email=register_in.email)

    user = User(
        email=register_in.email,
        phone_number=register_in.phone_number,
        first_name=register_in.first_name,
        last_name=register_in.last_name,
        password=hash_pwd(register_in.password),
    )
    verification_url = create_verification_url(register_in.email)
    send_email(register_in.email, "Verification URL", verification_url)

    session.add(user)
    await session.commit()
    return RegisterResponse(email=register_in.email)
