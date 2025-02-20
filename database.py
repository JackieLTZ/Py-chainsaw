from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/ww"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def get_db():
    async with AsyncSessionLocal(bind=engine) as session:
        yield session



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close():
    await engine.dispose()