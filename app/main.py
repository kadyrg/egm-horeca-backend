from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import client, media, helper, admin, auth


description = """
    API endpoints:
        client: /api/docs
        admin: /admin/docs
        media: /media/docs
"""

app = FastAPI(
    title="EGM Horeca",
    summary="EGM Horeca API",
    description=description
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/api", client)
app.mount("/media", media)
app.mount("/admin", admin)
app.mount("/auth", auth)
app.include_router(helper.router)
