from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker, 
    async_scoped_session, 
    AsyncSession)

from src.config import settings
from typing import AsyncGenerator


class DataBase:
    def __init__(self, url: str, echo: bool = False) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        self.async_session = async_sessionmaker(bind=self.engine)


    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.async_session() as session:
            yield session


db = DataBase(url=settings.db_url)