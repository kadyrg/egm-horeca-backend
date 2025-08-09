from fastapi import FastAPI

from .products import router as product_router
from .categories import router as category_router


media = FastAPI(title='EGM Horeca Media')

media.include_router(product_router)
media.include_router(category_router)
