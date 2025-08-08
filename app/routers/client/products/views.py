from typing import List, Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Path
from sqlalchemy.ext.asyncio.session import AsyncSession
from PIL import Image, ImageOps
from io import BytesIO
import uuid

from app.db import get_db_session
from app.core import settings
from . import crud
from app.schemas import ProductList, ProductDetail, ProductDetailAll
from app.dependencies.language import language_dependency
from app.models import Product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/")
async def create_product(
    image: Annotated[UploadFile, File(...)],
    session: AsyncSession = Depends(get_db_session),
):
    image_bytes = await image.read()
    img = Image.open(BytesIO(image_bytes))

    target_width, target_height = 840, 1008

    # Resize image proportionally so that it covers the target size (like object-cover)
    img = ImageOps.fit(img, (target_width, target_height), method=Image.LANCZOS, centering=(0.5, 0.5))

    # Save image as WEBP with quality 100
    filename = f"{uuid.uuid4().hex}.webp"
    filepath = settings.media_url / "products" / filename
    img.save(filepath, format="WEBP", quality=100)

    # Assuming you want to create one product with this image (not inside a loop)
    # Or else your current loop overwrites all products with the same image (likely unintended)
    product = Product()
    product.image = f"/media/products/{filename}"
    session.add(product)
    await session.commit()

    return "Finished"


@router.get(
    path="",
    summary="Get products",
    description="Get products",
    response_model=List[ProductDetailAll],
)
async def get_products(
        language: str = Depends(language_dependency),
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_products(language, session)


@router.get(
    path="/top",
    summary="Get top products",
    description="Get top products",
    response_model=List[ProductList],
)
async def get_top_products(
        language: str = Depends(language_dependency),
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_top_products(language, session)


@router.get(
    path="/new",
    summary="Get new products",
    description="Get new products",
    response_model=List[ProductList],
)
async def get_new_products(
        language: str = Depends(language_dependency),
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_new_products(language, session)

@router.get(
    path="/{slug}",
    summary="Get new products",
    description="Get new products",
    response_model=ProductDetail,
)
async def get_product(
        slug: Annotated[str, Path(...)],
        language: str = Depends(language_dependency),
        session: AsyncSession = Depends(get_db_session)
):
    return await crud.get_product(slug, language, session)
