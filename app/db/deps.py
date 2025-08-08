from typing import AsyncGenerator

from app.db.session import async_scoped_session_instance


async def get_db_session() -> AsyncGenerator:
    session = async_scoped_session_instance()
    try:
        yield session
    finally:
        await async_scoped_session_instance.remove()
