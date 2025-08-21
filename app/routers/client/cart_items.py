from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from typing import List

from app.db import get_db_session
from app.deps import get_user
from app.schemas import (
    CartItemCreate,
    CartItemList,
)
from app.models import User
from app.crud import (
    add_cart_item,
    get_cart_items,
)


router = APIRouter(prefix="/cart_items", tags=["Cart Items"])


@router.post("", response_model=CartItemList)
async def _add_cart_item(
    cart_item_in: CartItemCreate,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(get_db_session),
):
    return await add_cart_item(cart_item_in, user, session)


@router.get("", response_model=List[CartItemList])
async def _get_cart_items(
    user: User = Depends(get_user), session: AsyncSession = Depends(get_db_session)
):
    return await get_cart_items(user, session)
