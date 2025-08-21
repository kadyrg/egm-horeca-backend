from typing import Annotated
from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db_session
from app.models import MetaDataGroup
from app.crud import get_metadata_admin


router = APIRouter(prefix="/metadata", tags=["Metadata"])

@router.get('/{group}')
async def _get_metadata(
        group: Annotated[MetaDataGroup, Query(...)],
        session: AsyncSession = Depends(get_db_session),
):
    return await get_metadata_admin(group, session)
