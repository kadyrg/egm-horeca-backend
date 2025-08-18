from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db import get_db_session
from app.deps import get_user
from app.schemas import (
    UserProductLike,
    UserProductLikesBulkCreate
)
from app.models import User
from app.crud import (
    add_user_product_like,
    delete_user_product_like,
    get_user_product_likes,
    add_bulk_user_product_like
)


router = APIRouter(
    prefix="/user_product_likes",
    tags=["User Product Likes"]
)

@router.post('', response_model=UserProductLike)
async def _add_user_product_like(
        user_product_like_in: UserProductLike,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_db_session)
):
    return await add_user_product_like(user_product_like_in, user, session)

@router.get('', response_model=List[UserProductLike])
async def _get_user_product_like(
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_db_session)
):
    return await get_user_product_likes(user, session)

@router.delete('', response_model=UserProductLike)
async def _delete_user_product_like(
        user_product_like_in: UserProductLike,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_db_session)
):
    return await delete_user_product_like(user_product_like_in, user, session)

@router.post('/add_bulk', response_model=List[UserProductLike])
async def _add_bulk_user_product_like(
        user_product_likes_in: UserProductLikesBulkCreate,
        user: User = Depends(get_user),
        session: AsyncSession = Depends(get_db_session)
):
    return await add_bulk_user_product_like(user_product_likes_in, user, session)
