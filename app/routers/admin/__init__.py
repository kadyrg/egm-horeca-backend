from fastapi import FastAPI

from .categories import router as categories_router


app = FastAPI(
    title='Admin',
    prefix='/admin',
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    },
)

app.include_router(categories_router)
