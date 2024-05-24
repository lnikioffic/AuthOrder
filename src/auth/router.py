from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.schemas import UserCreate, UserRead, UserLogin
from src.auth.schemas import TokenInfo
from src.auth.dependencies import (
    validate_auth_user, 
    get_current_active_auth_user, 
    get_current_token_payload,
    refresh_token_jwt,
    get_current_auth_user_for_refresh
)
from src.users.dependencies import valid_user_id
from src.auth import service
from src.database import db

http_bearer = HTTPBearer(auto_error=False)
router = APIRouter(prefix='/auth', tags=['Auth'], dependencies=[Depends(http_bearer)])


@router.post('/singun', response_model=UserRead)
async def sing_up(user: UserCreate, session: AsyncSession = Depends(db.get_session)):
    res = await service.create_user(user, session)
    return res


@router.post('/singin', response_model=TokenInfo)
async def auth(token: Annotated[str, Depends(validate_auth_user)]):

    return token


@router.post(
        '/refresh',
        response_model=TokenInfo,
        response_model_exclude_none=True
    )
async def auth_refresh_jwt(user: Annotated[UserRead, Depends(get_current_auth_user_for_refresh)]):
    ref = await refresh_token_jwt(user)
    return ref


@router.get('/me')
async def get_me(
    payload: Annotated[dict, Depends(get_current_token_payload)],
    me: Annotated[UserRead, Depends(get_current_active_auth_user)]
    ):
    iat =  payload.get("iat")
    return {
        'username': me.username,
        'log': iat
    }    


@router.get('/users', response_model=list[UserRead])
async def get_user(session: AsyncSession = Depends(db.get_session)):
    res = await service.get_user(session)
    return res


# @router.get('/user/{user_id}', response_model=UserRead)
# async def get_user_id(user: Annotated[UserRead, Depends(valid_user_id)]):
#     return user
