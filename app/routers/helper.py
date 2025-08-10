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

@router.post("/price")
async def add_category_images(
        session: AsyncSession = Depends(get_db_session),
):
    result = await session.execute(select(Product))
    products = result.scalars().all()
    for product in products:
        product.status = random.choice([True, False])
    await session.commit()
    return "success"

