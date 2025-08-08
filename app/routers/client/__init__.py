from fastapi import APIRouter

from .metadata.views import router as features_router
from .categories.views import router as categories_router
from .products.views import router as products_router


router = APIRouter()

router.include_router(features_router)
router.include_router(categories_router)
router.include_router(products_router)
