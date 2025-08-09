from fastapi import UploadFile
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from math import ceil

from app.utils import save_category_image
from app.schemas import StatusRes, CategoryList, CategoryDetail, ProductList, Products, CategoryBase
from app.models import Category, Product, Conf, ConfType


async def add_category(name_en: str, name_ro: str, image: UploadFile, session: AsyncSession) -> StatusRes:
    image_bytes = await image.read()
    category = Category(
        name_en=name_en,
        name_ro=name_ro,
        image=save_category_image(image_bytes)
    )
    session.add(category)
    await session.commit()
    return StatusRes(status="success", message="Category added successfully")


async def get_categories(language: str, session: AsyncSession) -> List[CategoryList]:
    stmt = select(Category).join(Product).distinct()
    result = await session.execute(stmt)
    categories = result.scalars().all()
    return [
        CategoryList(
            id=category.id,
            name=getattr(category, f"name_{language}", category.name_en),
            slug=getattr(category, f"slug_{language}", category.slug_en)
        ) for category in categories
    ]


async def get_categories_admin(lang: str, session: AsyncSession) -> List[CategoryBase]:
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    return [
        CategoryBase(
            id=category.id,
            name=getattr(category, f"name_{lang}", category.name_en)
        ) for category in categories
    ]


async def get_category(slug: str, language: str, session: AsyncSession) -> CategoryDetail:
    slug_field = getattr(Category, f"slug_{language}", Category.slug_en)
    category_stmt = select(Category).where(slug_field==slug).join(Product).distinct()
    category_result = await session.execute(category_stmt)
    category = category_result.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    page_size_stmt = select(Conf).where(Conf.type == ConfType.page_size)
    page_size_result = await session.execute(page_size_stmt)
    page_size_conf = page_size_result.scalar_one()
    page_size = int(page_size_conf.value)

    count_stmt = select(func.count()).where(Product.category_id == category.id)
    count_result = await session.execute(count_stmt)
    total_products = count_result.scalar_one()

    total_pages = ceil(total_products / page_size)

    return CategoryDetail(
        id=category.id,
        name=getattr(category, f"name_{language}", category.name_en),
        slug=getattr(category, f"slug_{language}", category.slug_en),
        image=category.image,
        total_products=total_products,
        total_pages=total_pages,
    )





async def get_category_products(slug: str, language: str, page: int, session: AsyncSession) -> Products:
    slug_field = getattr(Category, f"slug_{language}", Category.slug_en)
    category_stmt = select(Category).where(slug_field==slug)
    category_result = await session.execute(category_stmt)
    category = category_result.scalar_one_or_none()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")

    page_size_stmt = select(Conf).where(Conf.type == ConfType.page_size)
    page_size_result = await session.execute(page_size_stmt)
    page_size_conf = page_size_result.scalar_one()
    page_size = int(page_size_conf.value)

    products_stmt = (
        select(Product)
        .where(Product.category_id == category.id)
        .order_by(Product.created_at.desc())
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    products_result = await session.execute(products_stmt)
    products = products_result.scalars().all()

    count_stmt = select(func.count()).where(Product.category_id == category.id)
    count_result = await session.execute(count_stmt)
    total_products = count_result.scalar_one()

    total_pages = ceil(total_products / page_size)

    return Products(
        total_pages=total_pages,
        current_page=page,
        total_products=total_products,
        products=[
            ProductList(
                id=product.id,
                name=getattr(product, f"name_{language}", product.name_en),
                description=getattr(product, f"description_{language}", product.description_en),
                image=product.image,
                price=product.price,
                slug=getattr(product, f"slug_{language}", product.slug_en)
            ) for product in products
        ]
    )
