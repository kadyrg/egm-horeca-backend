from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict


class TokenResponse(BaseModel):
    access_token: Annotated[str, Field(alias='accessToken')]
    refresh_token: Annotated[str, Field(alias='refreshToken')]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
