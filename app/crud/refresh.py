from app.models import User
from app.schemas import TokenResponse
from app.utils import generate_access_token, generate_refresh_token


async def refresh(user: User) -> TokenResponse:
    return TokenResponse(
        access_token=generate_access_token(user),
        refresh_token=generate_refresh_token(user),
    )
