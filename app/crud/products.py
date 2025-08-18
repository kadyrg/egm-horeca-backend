from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
import json
from slugify import slugify

from app.models import (
    Product,
    Conf,
    ConfType,
    User, ProductVariant
)
from app.schemas import (
    ProductList,
    ProductDetail,
    CategoryList,
    ProductListAdmin,
    StatusRes,
    ProductListView,
    ProductsForSearch,
    ProductIn
)
from app.utils import (
    save_product_image,
    delete_media_file
)


async def get_products_admin(
        page: int,
        session: AsyncSession
) -> ProductListAdmin:
    total_stmt = select(func.count(Product.id))
    total_result = await session.execute(total_stmt)
    total = total_result.scalar_one()
    stmt = (
        select(
            Product,
            func.count(ProductVariant.id).label("variants_count")
        )
        .join(
            ProductVariant,
            ProductVariant.product_id == Product.id,
            isouter=True
        )
        .group_by(Product.id)
        .order_by(-Product.id)
        .offset((page - 1) * 25)
        .limit(25)
    )
    result = await session.execute(stmt)
    rows = result.all()
    products = [
        ProductListView.model_validate(
            {**product.__dict__, "variants_count": variants_count}
        )
        for product, variants_count in rows
    ]
    return ProductListAdmin(
        data=[ProductListView.model_validate(product) for product in products],
        total=total,
        initial=(page - 1) * 25 + 1 if products else 0,
        last=(page - 1) * 25 + len(products),
        total_pages=(total + 25 - 1) // 25,
        page=page
    )

async def add_product_admin(
        product_in: str,
        main_image: UploadFile | None,
        extra_image_1: UploadFile | None,
        extra_image_2: UploadFile | None,
        extra_image_3: UploadFile | None,
        extra_image_4: UploadFile | None,
        extra_image_5: UploadFile | None,
        extra_image_6: UploadFile | None,
        session: AsyncSession
) -> ProductListView:
    product_in_data = json.loads(product_in)
    validated = ProductIn(**product_in_data)
    image_files = [main_image, extra_image_1, extra_image_2, extra_image_3,
                   extra_image_4, extra_image_5, extra_image_6]
    image_paths = []
    for img in image_files:
        if img:
            image_bytes = await img.read()
            image_paths.append(save_product_image(image_bytes))
        else:
            image_paths.append(None)

    product = Product(
        name_en=validated.name_en,
        name_ro=validated.name_ro,
        description_en=validated.description_en,
        description_ro=validated.description_ro,
        category_id=validated.category_id,
        price=validated.price,
        stock=validated.stock,
        status=validated.status,
        is_top=validated.is_top,
        slug_en=slugify(validated.name_en),
        slug_ro=slugify(validated.name_ro),
        main_image=image_paths[0],
        extra_image_1=image_paths[1],
        extra_image_2=image_paths[2],
        extra_image_3=image_paths[3],
        extra_image_4=image_paths[4],
        extra_image_5=image_paths[5],
        extra_image_6=image_paths[6],
    )
    session.add(product)
    await session.commit()
    return ProductListView.model_validate(product)


async def update_product_admin(
        product_id: int,
        product_in: str,
        main_image: UploadFile | None,
        extra_image_1: UploadFile | None,
        extra_image_2: UploadFile | None,
        extra_image_3: UploadFile | None,
        extra_image_4: UploadFile | None,
        extra_image_5: UploadFile | None,
        extra_image_6: UploadFile | None,
        session: AsyncSession
) -> ProductListView:
    stmt = (
        select(Product)
        .where(Product.id == product_id)
    )
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    product_in_data = json.loads(product_in)
    validated = ProductIn(**product_in_data)
    old_paths = [
        product.main_image,
        product.extra_image_1,
        product.extra_image_2,
        product.extra_image_3,
        product.extra_image_4,
        product.extra_image_5,
        product.extra_image_6
    ]
    new_files = [main_image, extra_image_1, extra_image_2, extra_image_3,
                 extra_image_4, extra_image_5, extra_image_6]
    new_paths = []
    for old_path, new_file in zip(old_paths, new_files):
        if new_file:
            image_bytes = await new_file.read()
            new_path = save_product_image(image_bytes)
            new_paths.append(new_path)
            delete_media_file(old_path)
        else:
            new_paths.append(old_path)
    (
        product.main_image,
        product.extra_image_1,
        product.extra_image_2,
        product.extra_image_3,
        product.extra_image_4,
        product.extra_image_5,
        product.extra_image_6
    ) = new_paths
    product.name_en=validated.name_en
    product.name_ro=validated.name_ro
    product.description_en=validated.description_en
    product.description_ro=validated.description_ro
    product.category_id=validated.category_id
    product.price=validated.price
    product.stock=validated.stock
    product.status=validated.status
    product.is_top=validated.is_top
    product.slug_en=slugify(validated.name_en)
    product.slug_ro=slugify(validated.name_ro)
    await session.commit()
    return ProductListView.model_validate(product)


async def delete_products_admin(
        product_id: int,
        session: AsyncSession
) -> StatusRes:
    stmt = (
        select(Product)
        .where(Product.id == product_id)
    )
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    images_to_delete = [
        product.main_image,
        product.extra_image_1,
        product.extra_image_2,
        product.extra_image_3,
        product.extra_image_4,
        product.extra_image_5,
        product.extra_image_6,
    ]
    for image in images_to_delete:
        delete_media_file(image)
    await session.delete(product)
    await session.commit()
    return StatusRes(
        status="success",
        message="Product deleted"
    )

# Client

async def get_top_products(
        lang: str,
        session: AsyncSession
) -> List[ProductList]:
    stmt = (
        select(Product)
        .where(Product.is_top)
    )
    result = await session.execute(stmt)
    products = result.scalars().all()
    return [
        ProductList(
            id=product.id,
            name=getattr(product, f"name_{lang}", product.name_en),
            description=getattr(product, f"description_{lang}", product.name_en),
            main_image=product.main_image,
            price=product.price,
            slug=getattr(product, f"slug_{lang}", product.slug_en)
        ) for product in products
    ]

async def get_new_products(
        lang: str,
        session: AsyncSession
) -> List[ProductList]:
    count_stmt = (
        select(Conf)
        .where(Conf.type==ConfType.new_products_count)
    )
    count_result = await session.execute(count_stmt)
    count_conf = count_result.scalar_one_or_none()
    if count_conf is None:
        raise HTTPException(
            status_code=404,
            detail="The new_products count is None"
        )
    count = int(count_conf.value)
    stmt = (
        select(Product)
        .order_by(Product.created_at.desc())
        .limit(count)
    )
    result = await session.execute(stmt)
    products = result.scalars().all()
    return [
        ProductList(
            id=product.id,
            name=getattr(product, f"name_{lang}", product.name_en),
            description=getattr(product, f"description_{lang}", product.name_en),
            main_image=product.main_image,
            price=product.price,
            slug=getattr(product, f"slug_{lang}", product.slug_en)
        ) for product in products
    ]

async def get_products(
        session: AsyncSession
) -> List[ProductsForSearch]:
    stmt = select(Product)
    result = await session.execute(stmt)
    products = result.scalars().all()
    return [ProductsForSearch.model_validate(product) for product in products]



# Above don't touch

async def get_product(
        slug: str,
        lang: str,
        session: AsyncSession
) -> ProductDetail:
    slug_field = getattr(Product, f"slug_{lang}", Product.slug_en)
    product_stmt = (
        select(Product)
        .options(selectinload(Product.category))
        .where(slug_field == slug)
    )
    product_result = await session.execute(product_stmt)
    product = product_result.scalar_one_or_none()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return ProductDetail(
        id=product.id,
        name=getattr(product, f"name_{lang}", product.name_en),
        description=getattr(product, f"description_{lang}", product.description_en),
        main_image=product.main_image,
        price=product.price,
        category=CategoryList(
            id=product.category.id,
            name=getattr(product.category, f"name_{lang}", product.category.name_en),
            slug=getattr(product.category, f"slug_{lang}", product.category.slug_en),
        )
    )

async def get_liked_products(
        lang: str,
        user: User,
        session: AsyncSession
) -> List[ProductList]:
    stmt = select(Product).join(Product.liked_users).where(
        User.id == user.id
    )
    result = await session.execute(stmt)
    products = result.scalars().all()
    return [
        ProductList(
            id=product.id,
            name=getattr(product, f"name_{lang}", product.name_en),
            description=getattr(product, f"description_{lang}", product.name_en),
            image=product.image,
            price=product.price,
            slug=getattr(product, f"slug_{lang}", product.slug_en)
        ) for product in products
    ]
