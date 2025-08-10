from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Product, Conf, ConfType
from app.schemas import ProductList, ProductDetail, CategoryList, ProductDetailAll, ProductListAdmin, CategoryAdminList


async def get_products(session: AsyncSession) -> List[ProductDetailAll]:
    stmt = select(Product)
    result = await session.execute(stmt)
    products = result.scalars().all()
    return [ProductDetailAll.model_validate(product) for product in products]


async def get_top_products(language: str, session: AsyncSession) -> List[ProductList]:
    stmt = select(Product)
    result = await session.execute(stmt)
    products = result.scalars().all()
    return [
        ProductList(
            id=product.id,
            name=getattr(product, f"name_{language}", product.name_en),
            description=getattr(product, f"description_{language}", product.name_en),
            image=product.image,
            price=product.price,
            slug=getattr(product, f"slug_{language}", product.slug_en)
        ) for product in products
    ]


async def get_products_admin(session: AsyncSession) -> List[ProductListAdmin]:
    result = await session.execute(select(Product).options(selectinload(Product.category)).order_by(Product.id.desc()))
    products = result.scalars().all()
    return [ProductListAdmin.model_validate(product) for product in products]


async def get_new_products(language: str, session: AsyncSession) -> List[ProductList]:
    count_stmt = select(Conf).where(Conf.type==ConfType.new_products_count)
    count_result = await session.execute(count_stmt)
    count_conf = count_result.scalar_one_or_none()
    if count_conf is None:
        raise HTTPException(status_code=404, detail="The new_products count is None")
    count = int(count_conf.value)
    stmt = select(Product).order_by(Product.created_at.desc()).limit(count)
    result = await session.execute(stmt)
    products = result.scalars().all()
    return [
        ProductList(
            id=product.id,
            name=getattr(product, f"name_{language}", product.name_en),
            description=getattr(product, f"description_{language}", product.name_en),
            image=product.image,
            price=product.price,
            slug=getattr(product, f"slug_{language}", product.slug_en)
        ) for product in products
    ]


async def get_product(slug: str, language: str, session: AsyncSession) -> ProductDetail:
    slug_field = getattr(Product, f"slug_{language}", Product.slug_en)
    product_stmt = select(Product).options(selectinload(Product.category)).where(slug_field == slug)
    product_result = await session.execute(product_stmt)
    product = product_result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductDetail(
        id=product.id,
        name=getattr(product, f"name_{language}", product.name_en),
        description=getattr(product, f"description_{language}", product.description_en),
        image=product.image,
        price=product.price,
        category=CategoryList(
            id=product.category.id,
            name=getattr(product.category, f"name_{language}", product.category.name_en),
            slug=getattr(product.category, f"slug_{language}", product.category.slug_en),
        )
    )
