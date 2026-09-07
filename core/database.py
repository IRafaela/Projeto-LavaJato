from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from core.configs import settings

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session: AsyncSession = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)

async def get_session()-> AsyncGenerator:
    db: AsyncSession = Session()
    try:
        yield db
    finally:   
        await db.close()