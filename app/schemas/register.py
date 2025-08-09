from typing import Annotated

from pydantic import BaseModel, Field, EmailStr


class Register(BaseModel):
    email: Annotated[EmailStr, Field(..., alias='email')]
    phone_number: Annotated[str, Field(alias='phoneNumber')]
    first_name: Annotated[str, Field(..., alias='firstName')]
    last_name: Annotated[str, Field(..., alias='lastName')]
    password: Annotated[str, Field(..., alias='password')]


class RegisterResponse(BaseModel):
    email: Annotated[str, Field(alias='email')]
