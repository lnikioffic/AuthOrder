from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result
from sqlalchemy import select
from fastapi import Depends, HTTPException, status

from src.users.schemas import UserCreate, UserRead
from src.users.models import User
from src.auth import utils as auth_utils


async def get_user(session: AsyncSession) -> list[UserRead]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def create_user(user: UserCreate, session: AsyncSession) -> UserRead:
    stmt = select(User).filter(User.email == user.email)
    result = await session.execute(stmt)
    user_exists = result.scalars().all()
    if len(user_exists) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user.hashed_password = auth_utils.hash_password(user.hashed_password).decode()
    add_user = User(**user.model_dump())
    session.add(add_user)
    await session.commit()
    return add_user
