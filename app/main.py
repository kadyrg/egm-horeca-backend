from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import client_router, admin_app
from .routers.helper import router as helper_router


app = FastAPI(
    title="EGM Horeca",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1
    },
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client_router)
app.include_router(helper_router)
app.mount("/admin", admin_app)
