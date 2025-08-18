from fastapi import FastAPI

from .login import router as login_router
from .refresh import router as refresh_router
from .register import router as register_router
from .verify import router as verify_router

app = FastAPI(
    title="EGM Horeca Auth",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    },
)

app.include_router(login_router)
app.include_router(refresh_router)
app.include_router(register_router)
app.include_router(verify_router)
