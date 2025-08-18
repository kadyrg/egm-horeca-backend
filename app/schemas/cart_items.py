from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class CartItemCreate(BaseModel):
    product_id: Annotated[int, Field(ge=1, alias="productId")]

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)


class CartItemList(BaseModel):
    product_id: Annotated[str, Field(alias="productId")]
    quantity: str

    model_config = ConfigDict(from_attributes=True, validate_by_name=True)
