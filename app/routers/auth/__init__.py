from fastapi import APIRouter

from .login.views import router as login_router
from .register.views import router as register_router
from .verify.views import router as verify_router


router = APIRouter()

router.include_router(login_router)
router.include_router(register_router)
router.include_router(verify_router)
