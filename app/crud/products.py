from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import Product, Conf, ConfType, ProductExtraImages
from app.schemas import (
    ProductList,
    ProductDetail,
    CategoryList,
    ProductDetailAll,
    ProductListAdmin,
    CategoryAdminList,
    StatusRes, ProductDetailAdmin,
)
from app.deps import ProductCreate, ProductUpdate
from app.utils import save_product_image


async def add_product(product_in: ProductCreate, session: AsyncSession) -> StatusRes:
    image_bytes = await product_in.image.read()
    image_path = save_product_image(image_bytes)
    product = Product(
        name_ro=product_in.name_ro,
        name_en=product_in.name_en,
        description_ro=product_in.description_ro,
        description_en=product_in.description_en,
        category_id=product_in.category_id,
        price=product_in.price,
        stock=product_in.stock,
        status=product_in.status,
        slug_en = product_in.slug_en,
        slug_ro = product_in.slug_ro,
        image=image_path,
    )
    session.add(product)
    await session.flush()
    for extra_image in product_in.extra_images:
        extra_image_bytes = await extra_image.extra_image.read()
        extra_image_path = save_product_image(extra_image_bytes)
        product_extra_image = ProductExtraImages(
            order=extra_image.order,
            image=extra_image_path,
            product_id=product.id,
        )
        session.add(product_extra_image)
    await session.commit()
    return StatusRes(status="success", message="Product added successfully")


async def get_product_admin(product_id: int, session: AsyncSession) -> ProductDetailAdmin:
    stmt = (select(Product)
            .where(Product.id == product_id)
            .options(selectinload(Product.extra_images), selectinload(Product.category)))
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductDetailAdmin.model_validate(product)


async def get_products_admin(session: AsyncSession) -> List[ProductListAdmin]:
    result = await session.execute(select(Product).options(selectinload(Product.category)).order_by(Product.id.desc()))
    products = result.scalars().all()
    return [ProductListAdmin.model_validate(product) for product in products]


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


async def update_product(product_id: int, product_in: ProductUpdate, session: AsyncSession) -> StatusRes:
    result = await session.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    product_data = product_in.dict(exclude_none=True)
    for key, value in product_data.items():
        setattr(product, key, value)
    if product_in.image:
        image_bytes = await product_in.image.read()
        image_path = save_product_image(image_bytes)
        product.image = image_path
    await session.commit()
    return StatusRes(status="success", message="Product updated")
