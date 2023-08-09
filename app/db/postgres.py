from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import get_settings

# Get application settings
settings = get_settings()
# Create an asynchronous engine for the database
engine = create_async_engine(
    f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    echo=True,  # Set to True for debugging SQL statements (optional)
    future=True,  # Enable future mode for improved performance
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_recycle=settings.DB_POOL_RECYCLE,
)


@asynccontextmanager
async def get_session() -> AsyncSession:
    """
    Asynchronous context manager to acquire and release database sessions.

    Returns:
    - AsyncSession: An asynchronous database session object.
    """
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
