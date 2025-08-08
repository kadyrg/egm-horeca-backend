from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import MetaData, MetaDataGroup


async def get_metadata(language: str, group: MetaDataGroup, session: AsyncSession) -> dict:
    stmt = select(MetaData).where(MetaData.type == group)
    result = await session.execute(stmt)
    page = result.scalar_one()
    metadata = page.value.get(language, page.value.get("en"))
    return metadata
