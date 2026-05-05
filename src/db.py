"""Database connection and session factory for Postgres (async).

Replace `DATABASE_URL` with real credentials or load from env/config.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# TODO: Load from environment/config securely
DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/dbname"

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_session():
    """Yield an async DB session. Use with dependency injection in FastAPI.

    Example (FastAPI):
        async for session in get_session():
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session
