from fastapi import FastAPI

from .categories import router as categories_router
from .products import router as products_router


media = FastAPI(
    title='Media',
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    },
)

media.include_router(products_router)
media.include_router(categories_router)
