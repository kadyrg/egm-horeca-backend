from fastapi import FastAPI

from .client import router as client_router
from .media import router as media_router
from .admin import router as admin_router
from .auth import router as auth_router


client_description = """
    EGM Horeca Client API
"""

client = FastAPI(
    title="EGM Horeca Client",
    summary="EGM Horeca Client API",
    description=client_description,
)

client.include_router(client_router)


media_description = """
    EGM Horeca Media API
"""

media = FastAPI(
    title="EGM Horeca Media",
    summary="EGM Horeca Media API",
    description=media_description,
)

media.include_router(media_router)


admin_description = """
    EGM Horeca Media API
"""

admin = FastAPI(
    title="EGM Horeca Admin",
    summary="EGM Horeca Admin API",
    description=admin_description,
)

admin.include_router(admin_router)


auth_description = """
    EGM Horeca Authentication API
"""

auth = FastAPI(
    title="EGM Horeca Authentication",
    summary="EGM Horeca Authentication API",
    description=auth_description,
)

auth.include_router(auth_router)
