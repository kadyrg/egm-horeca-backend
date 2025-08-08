from PIL import Image, ImageOps
from io import BytesIO
import uuid

from app.core import settings


async def save_product_image(image_bytes: bytes) -> str:
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
