from pydantic import BaseModel


class StatusRes(BaseModel):
    status: str
    message: str
