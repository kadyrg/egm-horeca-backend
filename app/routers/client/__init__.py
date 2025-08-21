from fastapi import FastAPI

from .categories import router as categories_router
from .products import router as products_router
from .metadata import router as metadata_router
from .cart_items import router as cart_items_router
from .user_product_likes import router as user_product_likes_router
from .banners import router as banners_router


app = FastAPI(
    title="EGM Horeca Client",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(metadata_router)
app.include_router(cart_items_router)
app.include_router(user_product_likes_router)
app.include_router(banners_router)
