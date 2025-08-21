from fastapi import UploadFile, Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from fastapi import HTTPException
from math import ceil
from slugify import slugify
import json

from app.utils import save_category_image, delete_media_file
from app.schemas import (
    StatusRes,
    CategoryList,
    CategoryDetail,
    ProductList,
    CategoryIn,
    CategoryListAdmin,
    CategoryListView,
    CategoryListViewAll,
    CategoryInResponse,
)
from app.models import Category, Product, Conf, ConfType, ProductVariant

# Admin


async def add_category_admin(
    category_in: str, image: UploadFile, session: AsyncSession
) -> CategoryInResponse:
    category_in_data = json.loads(category_in)
    validated = CategoryIn(**category_in_data)
    image_bytes = await image.read()
    image_path = save_category_image(image_bytes)
    category = Category(
        name_en=validated.name_en,
        name_ro=validated.name_ro,
        slug_en=slugify(validated.name_en),
        slug_ro=slugify(validated.name_ro),
        image=image_path,
    )
    session.add(category)
    await session.commit()
    return CategoryInResponse.model_validate(category)


async def get_categories_admin(page: int, session: AsyncSession) -> CategoryListAdmin:
    total_stmt = select(func.count(Category.id))
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()
    stmt = (
        select(Category, func.count(Product.id).label("product_count"))
        .join(Product, Product.category_id == Category.id, isouter=True)
        .group_by(Category.id)
        .order_by(-Category.id)
        .offset((page - 1) * 25)
        .limit(25)
    )
    result = await session.execute(stmt)
    rows = result.all()
    categories = [
        CategoryListView.model_validate(
            {**category.__dict__, "product_count": product_count}
        )
        for category, product_count in rows
    ]
    return CategoryListAdmin(
        data=categories,
        total=total,
        initial=(page - 1) * 25 + 1 if categories else 0,
        last=(page - 1) * 25 + len(categories),
        total_pages=(total + 25 - 1) // 25,
        page=page,
    )


async def get_all_categories_admin(session: AsyncSession) -> List[CategoryListViewAll]:
    stmt = select(Category).order_by(-Category.id)
    result = await session.execute(stmt)
    categories = result.scalars().all()
    return [CategoryListViewAll.model_validate(category) for category in categories]


async def delete_category_admin(category_id: int, session: AsyncSession) -> StatusRes:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    delete_media_file(category.image)
    await session.delete(category)
    await session.commit()
    return StatusRes(
        status="success",
        message="Category deleted successfully",
    )


async def update_category_admin(
    category_id: int, category_in: str, image: UploadFile | None, session: AsyncSession
) -> CategoryListView:
    stmt = select(Category).where(Category.id == category_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    category_in_data = json.loads(category_in)
    validated = CategoryIn(**category_in_data)
    image_to_delete: str | None = None
    if image:
        image_to_delete = category.image
        image_bytes = await image.read()
        new_image_path = save_category_image(image_bytes)
        category.image = new_image_path
    category.name_en = validated.name_en
    category.name_ro = validated.name_ro
    category.slug_en = slugify(validated.name_en)
    category.slug_ro = slugify(validated.name_ro)
    await session.commit()
    if image_to_delete:
        delete_media_file(image_to_delete)
    return CategoryListView.model_validate(category)


# Client


async def get_categories(lang: str, session: AsyncSession) -> List[CategoryList]:
    stmt = select(Category).join(Product).distinct()
    result = await session.execute(stmt)
    categories = result.scalars().all()
    return [
        CategoryList(
            id=category.id,
            name=getattr(category, f"name_{lang}"),
            slug=getattr(category, f"slug_{lang}"),
        )
        for category in categories
    ]


async def get_category(request: Request, slug: str, lang: str, session: AsyncSession) -> CategoryDetail:
    slug_attr = getattr(Category, f"slug_{lang}", Category.slug_en)
    stmt = select(Category).where(slug_attr == slug)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()
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
    base_url = str(request.base_url)
    return CategoryDetail(
        id=category.id,
        name=getattr(category, f"name_{lang}"),
        slug=getattr(category, f"slug_{lang}"),
        image=f"{base_url}{category.image}",
        total_products=total_products,
        total_pages=total_pages,
    )


# Above don't touch


async def get_category_products(
    request: Request, slug: str, lang: str, page: int, session: AsyncSession
) -> List[ProductList]:
    slug_field = getattr(Category, f"slug_{lang}", Category.slug_en)
    category_stmt = select(Category).where(slug_field == slug)
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
    base_url = str(request.base_url)
    return [
        ProductList(
            id=product.id,
            name=getattr(product, f"name_{lang}", product.name_en),
            description=getattr(product, f"description_{lang}", product.description_en),
            main_image=f"{base_url}{product.main_image}",
            price=product.price,
            slug=getattr(product, f"slug_{lang}", product.slug_en),
        )
        for product in products
    ]
