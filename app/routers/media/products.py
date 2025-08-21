from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core import settings


router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/{image_name}")
async def get_product_image(image_name: str):
    image_path = settings.media_url / "products" / image_name
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(image_path)
