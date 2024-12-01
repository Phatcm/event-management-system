from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import Config

# Define async orm engine object
async_engine = AsyncEngine(create_engine(url=Config.DATABASE_URL, echo=True))


# This function handle the initialize start of db
async def init_db():
    async with async_engine.begin() as conn:
        from src.db.models import Event

        # Create all the SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)


# Dependency injection to create session accross all routes
async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,  # allow to use session after commit
    )

    async with Session() as session:
        yield session
