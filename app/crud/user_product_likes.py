from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.models import User, Product, user_product_likes
from app.schemas import UserProductLike, UserProductLikesBulkCreate


async def add_user_product_like(
    user_product_like_in: UserProductLike, user: User, session: AsyncSession
) -> UserProductLike:
    result = await session.execute(
        select(Product).where(Product.id == user_product_like_in.product_id)
    )
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await session.execute(
        user_product_likes.insert().values(
            user_id=user.id, product_id=user_product_like_in.product_id
        )
    )
    await session.commit()
    return user_product_like_in


async def get_user_product_likes(
    user: User, session: AsyncSession
) -> List[UserProductLike]:
    result = await session.execute(
        user_product_likes.select().where(user_product_likes.c.user_id == user.id)
    )
    user_likes = result.all()
    return [
        UserProductLike(product_id=user_like.product_id) for user_like in user_likes
    ]


async def delete_user_product_like(
    user_product_like_in: UserProductLike, user: User, session: AsyncSession
) -> UserProductLike:
    result = await session.execute(
        select(Product).where(Product.id == user_product_like_in.product_id)
    )
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    await session.execute(
        user_product_likes.delete().where(
            (user_product_likes.c.user_id == user.id)
            & (user_product_likes.c.product_id == user_product_like_in.product_id)
        )
    )
    await session.commit()
    return user_product_like_in


async def add_bulk_user_product_like(
    user_product_likes_in: UserProductLikesBulkCreate, user: User, session: AsyncSession
) -> List[UserProductLike]:
    result = await session.execute(
        user_product_likes.select().where(user_product_likes.c.user_id == user.id)
    )
    user_likes = result.all()
    existing_product_ids = {like.product_id for like in user_likes}
    product_ids_to_add = [
        pid
        for pid in user_product_likes_in.product_ids
        if pid not in existing_product_ids
    ]

    if product_ids_to_add:
        await session.execute(
            user_product_likes.insert(),
            [{"user_id": user.id, "product_id": pid} for pid in product_ids_to_add],
        )
    await session.commit()
    return [UserProductLike(product_id=product_id) for product_id in product_ids_to_add]
