from .admin import app as admin_app
from .client import router as client_router
from .media import media as media_app


__all__ = [
    'admin_app',
    'client_router',
    'media_app'
]
