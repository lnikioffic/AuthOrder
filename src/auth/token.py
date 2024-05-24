from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from src.users.schemas import UserLogin, UserRead
from src.auth.schemas import TokenInfo
from src.auth import utils as auth_utils
from src.auth.config import auth_jwt


TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'

async def create_token(
        token_type: str, 
        payload: dict, 
        expire_minutes: int = auth_jwt.access_token_expire_minutes, 
        expire_timedelta: timedelta | None = None
    ) -> str:

    jwt_payload = {
        TOKEN_TYPE_FIELD: token_type
    }

    jwt_payload.update(payload)

    return auth_utils.encode_jwt(
        payload=jwt_payload, 
        expire_minutes=expire_minutes, 
        expire_timedelta=expire_timedelta
    )


async def create_access_token(user: UserLogin) -> str:
    payload = {
        'sub': str(user.id),
        'user': {
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active
        }
    }

    return await create_token(
        token_type=ACCESS_TOKEN_TYPE, 
        payload=payload,
        expire_minutes=auth_jwt.access_token_expire_minutes
    )


async def create_refresh_token(user: UserLogin) -> str:
    payload = {
        'sub': str(user.id),
        # 'user': {
        #     'username': user.username,
        #     'email': user.email,
        #     'is_active': user.is_active
        # }
    }

    return await create_token(
        token_type=REFRESH_TOKEN_TYPE, 
        payload=payload,
        expire_timedelta=timedelta(days=auth_jwt.refresh_token_expire_days)
    )