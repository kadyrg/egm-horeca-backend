from .admin import app as admin_app
from .client import app as client_app
from .media import app as media_app
from .auth import app as auth_app

__all__ = ["admin_app", "client_app", "media_app", "auth_app"]
