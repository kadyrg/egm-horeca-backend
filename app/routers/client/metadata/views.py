from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db import get_db_session
from app.dependencies import language_dependency
from .utils import get_metadata
from app.models import MetaDataGroup
from .schemas import Website


router = APIRouter(
    prefix="/metadata",
    tags=["Metadata"]
)

@router.get(
    path="/website",
    summary="Website Metadata",
    description="Website Metadata",
    response_model=Website,
)
async def get_website_metadata(
        language: str = Depends(language_dependency),
        session: AsyncSession = Depends(get_db_session)
):
    metadata = await get_metadata(language, MetaDataGroup.website, session)
    return Website.model_validate(metadata)
