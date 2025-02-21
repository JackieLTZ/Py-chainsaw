from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.pool import AsyncAdaptedQueuePool



from models import Base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/w"

engine = create_async_engine(DATABASE_URL, echo=False, poolclass=AsyncAdaptedQueuePool,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30)

AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

async def check_db_connection():
    if engine.pool is None:
        raise RuntimeError("Database engine is not initialized.")
    
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1") ) 
        print("Database connection successful.")
    except Exception as e:
        raise RuntimeError("Failed to connect to the database.") from e
    

async def get_db():
    async with AsyncSessionLocal(bind=engine) as session:
        yield session



async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close():
    if engine is not None:
        await engine.dispose(close=True)