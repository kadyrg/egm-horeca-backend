from fastapi import FastAPI

from .categories import router as categories_router
from .products import router as products_router


app = FastAPI(
    title='Media',
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    },
)

app.include_router(products_router)
app.include_router(categories_router)
