from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.schemas import CartItemCreate, CartItemList
from app.models import User, Cart, CartItem


async def add_cart_item(
    cart_item_in: CartItemCreate, user: User, session: AsyncSession
) -> CartItemList:
    cart_stmt = select(Cart).where(Cart.user_id == user.id)
    cart_result = await session.execute(cart_stmt)
    cart = cart_result.scalar_one_or_none()
    if cart is None:
        cart = Cart(user_id=user.id)
        session.add(cart)
        await session.flush()

    cart_item_stmt = select(CartItem).where(
        CartItem.cart_id == cart.id, CartItem.product_id == cart_item_in.product_id
    )
    cart_item_result = await session.execute(cart_item_stmt)
    cart_item = cart_item_result.scalar_one_or_none()
    if cart_item:
        cart_item.quantity = cart_item.quantity + 1
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=cart_item_in.product_id,
            quantity=1,
        )
        session.add(cart_item)
    await session.commit()
    return CartItemList(
        product_id=str(cart_item.product_id),
        quantity=str(cart_item.quantity),
    )


async def get_cart_items(
    user: User,
    session: AsyncSession,
) -> List[CartItemList]:
    stmt = (
        select(Cart)
        .where(Cart.user_id == user.id)
        .options(selectinload(Cart.cart_items))
    )
    result = await session.execute(stmt)
    cart = result.scalar_one_or_none()
    if cart is None:
        cart = Cart(user_id=user.id)
        session.add(cart)
        await session.flush()
    return [
        CartItemList(
            product_id=str(cart_item.product_id),
            quantity=str(cart_item.quantity),
        )
        for cart_item in cart.cart_items
    ]
