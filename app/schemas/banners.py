from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, List

# Admin

class BannerListView(BaseModel):
    id: int
    image: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class BannerListAdmin(BaseModel):
    data: Annotated[List[BannerListView], Field(..., alias="data")]
    total: Annotated[int, Field(ge=0, alias="total")]
    initial: Annotated[int, Field(ge=0, alias="initial")]
    last: Annotated[int, Field(ge=0, alias="last")]
    total_pages: Annotated[int, Field(ge=0, alias="totalPages")]
    page: Annotated[int, Field(ge=0, alias="page")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


# Client

class BannerList(BaseModel):
    id: int
    image: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
