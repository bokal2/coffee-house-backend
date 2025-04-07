from sqlalchemy.ext.asyncio import AsyncSession
from db.session import async_session


async def get_db() -> AsyncSession:  # type: ignore
    async with async_session() as session:
        yield session
