from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.schemas import UserCreate, UserRead, UserAuth
from src.auth.schemas import TokenInfo
from src.auth.dependencies import validate_auth_user, get_current_active_auth_user
from src.auth import service
from src.database import db

router = APIRouter(prefix='/auth', tags=['Auth'])



@router.post('/singin', response_model=TokenInfo)
async def auth(token: Annotated[str, Depends(validate_auth_user)]):

    return token


@router.post('/singun', response_model=UserRead)
async def sing_up(user: UserCreate, session: AsyncSession = Depends(db.get_session)):
    res = await service.create_user(user, session)
    return res


@router.get('/me' )
async def get_me(me: Annotated[dict, Depends(get_current_active_auth_user)]):
    return me


@router.get('/users', response_model=list[UserRead])
async def get_user(session: AsyncSession = Depends(db.get_session)):
    res = await service.get_user(session)
    return res

