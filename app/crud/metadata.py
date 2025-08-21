from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MetaDataGroup, MetaData


async def get_metadata(
    language: str, group: MetaDataGroup, session: AsyncSession
) -> dict:
    stmt = select(MetaData).where(MetaData.type == group)
    result = await session.execute(stmt)
    page = result.scalar_one()
    metadata = page.value.get(language, page.value.get("en"))
    return metadata


async def get_metadata_admin(group: MetaDataGroup, session: AsyncSession):
    stmt = select(MetaData).where(MetaData.type == group)
    result = await session.execute(stmt)
    page = result.scalar_one()

