from fastapi import FastAPI

from .metadata import router as features_router
from .categories import router as categories_router
from .products import router as products_router


client = FastAPI(title='EGM Horeca Client')

client.include_router(features_router)
client.include_router(categories_router)
client.include_router(products_router)
