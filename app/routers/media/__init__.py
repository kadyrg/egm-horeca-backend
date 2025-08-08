from fastapi import APIRouter

from .products.views import router as product_router
from .categories.views import router as category_router


router = APIRouter()

router.include_router(product_router)
router.include_router(category_router)
