from src.database import db
from src.models import Base

import asyncio


async def main():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(main())

