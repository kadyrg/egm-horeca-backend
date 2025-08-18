
from pydantic import BaseModel


class VerifyEmail(BaseModel):
    token: str

