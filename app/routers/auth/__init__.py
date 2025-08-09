from fastapi import FastAPI

from .login import router as login_router
from .register import router as register_router
from .verify import router as verify_router
from .refresh import router as refresh_router


auth = FastAPI(title="EGM Horeca | Authentication")

auth.include_router(login_router)
auth.include_router(register_router)
auth.include_router(verify_router)
auth.include_router(refresh_router)
