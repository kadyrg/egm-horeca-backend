from datetime import timezone, datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, UploadFile, File
from slugify import slugify
from typing import Annotated, List
from PIL import Image
from io import BytesIO
import uuid
from pydantic import BaseModel
import random

from app.db import get_db_session
from app.models import Category, Product
from app.core import settings
from app.utils import save_product_image


router = APIRouter(
    prefix="/helper",
    tags=["Helper"],
)

@router.post(
    path="/generate_category_slugs",
    summary="Generate category slugs",
)
async def generate_category_slugs(
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(Category))
    categories = result.scalars().all()
    for category in categories:
        category.slug_en = slugify(category.name_en)
        category.slug_ro = slugify(category.name_ro)
    await session.commit()
    return "Success"


class ProductCreate(BaseModel):
    name_en: str
    name_ro: str
    description_en: str
    description_ro: str


@router.post(
    path="/add_bulk_products",
    summary="Add bulk products",
)
async def add_bulk_products(
        products_in: List[ProductCreate],
        session: AsyncSession = Depends(get_db_session)
):

    for product in products_in:
        product = Product(
            name_en=product.name_en,
            name_ro=product.name_ro,
            description_en=product.description_en,
            description_ro=product.description_ro,
            slug_en=slugify(product.name_en),
            slug_ro=slugify(product.name_ro),
            category_id=2,
            image="image",
        )
        session.add(product)
    await session.commit()
    return "Success"


@router.post(
    path="/add_bulk_products_images",
    summary="Add bulk products",
)
async def add_bulk_products_images(
        image: UploadFile = File(...),
        session: AsyncSession = Depends(get_db_session)
):
    image_bytes = await image.read()
    result = await session.execute(select(Product).where(Product.category_id == 2))
    products = result.scalars().all()
    for product in products:
        image_url = await save_product_image(image_bytes)
        product.image = image_url
    await session.commit()
    return "Success"


@router.post(
    path="/update_product_created_date",
    summary="Update product's created date",
)
async def update_product_created_date(
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    for product in products:
        product.created_at = datetime.now(timezone.utc)
    await session.commit()
    return "Success"


@router.post(
    path="/generate_product_slugs",
    summary="Generate product slugs",
)
async def generate_product_slugs(
        session: AsyncSession = Depends(get_db_session)
):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    for product in products:
        product.slug_en = slugify(product.name_en)
        product.slug_ro = slugify(product.name_ro)
    await session.commit()
    return "Success"


TARGET_WIDTH = 1920
TARGET_HEIGHT = 384

@router.post("/")
async def add_category_images(
        image: Annotated[UploadFile, File(...)],
        session: AsyncSession = Depends(get_db_session),
):
    image_bytes = await image.read()
    img = Image.open(BytesIO(image_bytes))

    target_aspect = TARGET_WIDTH / TARGET_HEIGHT
    img_aspect = img.width / img.height

    if img_aspect > target_aspect:
        new_height = TARGET_HEIGHT
        new_width = int(new_height * img_aspect)
    else:
        new_width = TARGET_WIDTH
        new_height = int(new_width / img_aspect)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    left = (new_width - TARGET_WIDTH) // 2
    top = (new_height - TARGET_HEIGHT) // 2
    right = left + TARGET_WIDTH
    bottom = top + TARGET_HEIGHT

    img = img.crop((left, top, right, bottom))

    result = await session.execute(select(Category))
    categories = result.scalars().all()
    for category in categories:
        filename = f"{uuid.uuid4().hex}.webp"
        filepath = settings.media_url / "categories" / filename
        img.save(filepath, format="WEBP", quality=100)
        category.image = f"/media/categories/{filename}"
    await session.commit()
    return "Finished"

@router.post("/price")
async def add_category_images(
        session: AsyncSession = Depends(get_db_session),
):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    for product in products:
        product.price = 40.99
    await session.commit()
    return "Finished"

@router.post("/randprice")
async def randomize_price(
        session: AsyncSession = Depends(get_db_session),
):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    for product in products:
        product.price = round(random.uniform(1, 9999), 2)
    await session.commit()
    return "Finished"

@router.post("/price")
async def add_category_images(
        session: AsyncSession = Depends(get_db_session),
):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    for product in products:
        product.price = 40.99
    await session.commit()
    return "Finished"

@router.post("/get_admin_token")
async def get_admin_token(
        session: AsyncSession = Depends(get_db_session),
):
    user = U
    products = result.scalars().all()
    for product in products:
        product.price = round(random.uniform(1, 9999), 2)
    await session.commit()
    return "Finished"

