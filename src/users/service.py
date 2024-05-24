from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from fastapi import Depends, HTTPException, status

from src.users.schemas import UserLogin, UserRead
from src.users.models import User
from src.database import db


class ServiceUser():
    def __init__(self, session: AsyncSession = Depends(db.get_session)) -> None:
        self.session = session
        
        
    async def get_user_by_username(self, username: str) -> UserLogin:
        stmt = select(User).filter(User.username == username)
        result: Result = await self.session.execute(stmt)
        user = result.scalar()
        
        return user
    

    async def get_user_by_id(self, id: int) -> UserRead | None:
        # stmt = select(User).filter(User.id == id)
        # result: Result = await self.session.execute(stmt)
        # user = result.scalar()
        user = await self.session.get(User, id)
        return user


#service_user = ServiceUser()