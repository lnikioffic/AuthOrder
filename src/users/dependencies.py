from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from fastapi import Depends, HTTPException, status

from src.users.schemas import UserAuth
from src.users.models import User
from src.database import db

class GetUser():
    def __init__(self, session: AsyncSession = Depends(db.get_session)) -> None:
        self.session = session
        
    async def get_user_for_auth(self, username: str) -> UserAuth:
        stmt = select(User).filter(User.username == username)
        result: Result = await self.session.execute(stmt)
        user = result.scalar()
        return user
