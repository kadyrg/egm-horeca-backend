from asyncio import current_task
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, async_scoped_session

from app.core import settings


engine = create_async_engine(
    url=settings.db_url,
    echo=False
)

async_session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession
)

async_scoped_session_instance = async_scoped_session(
    session_factory=async_session_factory,
    scopefunc=current_task,
)
