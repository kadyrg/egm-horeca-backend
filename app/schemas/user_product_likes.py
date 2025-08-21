from typing import Annotated, List

from pydantic import BaseModel, Field, ConfigDict


class UserProductLike(BaseModel):
    product_id: Annotated[int, Field(alias="productId")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class UserProductLikesBulkCreate(BaseModel):
    product_ids: List[int] = Field(..., alias="productIds")

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
