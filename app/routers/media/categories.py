from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.core import settings


router = APIRouter(prefix='/categories', tags=['Categories'])




@router.get('/{image_name}')
async def get_category_image(image_name: str):
    image_path = settings.media_url / 'categories' / image_name
    if not image_path.exists() or not image_path.is_file():
        raise HTTPException(status_code=404, detail='Image not found')
    return FileResponse(image_path)

