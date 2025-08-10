import os

from PIL import Image, ImageOps
from io import BytesIO
import uuid

from app.core import settings


def save_product_image(image_bytes: bytes) -> str:
    img = Image.open(BytesIO(image_bytes))
    target_width, target_height = 840, 1008
    img = ImageOps.fit(
        img,
        (target_width, target_height),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    filename = f"{uuid.uuid4().hex}.webp"
    filepath = settings.media_url / "products" / filename
    img.save(filepath, format="WEBP", quality=100)
    return f"/media/products/{filename}"


TARGET_WIDTH = 1920
TARGET_HEIGHT = 384

def save_category_image(image_bytes: bytes) -> str:
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

    filename = f"{uuid.uuid4().hex}.webp"
    filepath = settings.media_url / "categories" / filename
    img.save(filepath, format="WEBP", quality=100)
    return f"/media/categories/{filename}"


def delete_media_file(filepath: str):
    full_path = settings.base_url / filepath
    try:
        os.remove(full_path)
    except:
        pass
