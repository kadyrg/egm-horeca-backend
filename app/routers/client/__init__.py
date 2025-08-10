from fastapi import APIRouter

from .categories import router as categories_router


router = APIRouter(prefix="/api")

router.include_router(categories_router)
