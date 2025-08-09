from fastapi import FastAPI

from .categories import router as categories_router


admin = FastAPI(title="EGM Horeca | Admin")

admin.include_router(categories_router)
