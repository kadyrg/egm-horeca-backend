from fastapi import FastAPI

from .categories import router as categories_router
from .products import router as products_router
from .users import router as users_router
from .product_variant_types import router as product_variant_types_router
from .product_variants import router as product_variants_router
from .banners import router as banners_router
from .product_instances import router as product_instances_router


app = FastAPI(
    title="Admin",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(users_router)
app.include_router(product_variant_types_router)
app.include_router(product_variants_router)
app.include_router(banners_router)
app.include_router(product_instances_router)
