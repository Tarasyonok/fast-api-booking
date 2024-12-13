from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

if settings.MODE == "TEST" or settings.MODE == "PROD":
    DATABASE_URL = f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"

else:
    DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

DATABASE_PARAM = {"poolclass": NullPool}
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAM)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
