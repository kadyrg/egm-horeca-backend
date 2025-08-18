from typing import Annotated
from pydantic import BaseModel, Field


class RefreshRes(BaseModel):
    access_token: Annotated[str, Field(alias="accessToken")]
    status: str
