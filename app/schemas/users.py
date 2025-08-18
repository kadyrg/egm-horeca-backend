from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)
from typing import (
    Annotated,
    List
)


# Admin

class UserListView(BaseModel):
    id: int
    first_name: Annotated[str, Field(..., alias="firstName")]
    last_name: Annotated[str, Field(..., alias="lastName")]
    email: Annotated[str, Field(..., alias="email")]
    phone_number: Annotated[str, Field(..., alias="phoneNumber")]
    is_active: Annotated[int, Field(..., alias="isActive")]
    is_verified: Annotated[int, Field(..., alias="isVerified")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class UserListAdmin(BaseModel):
    data: List[UserListView]
    total: int
    initial: int
    last: int
    total_pages: Annotated[int, Field(..., alias="totalPages")]
    page: int

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
