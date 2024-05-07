from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from src.auth.token import create_access_token, create_refresh_token, TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.users.dependencies import GetUser
from src.users.schemas import UserAuth, UserRead
from src.auth.schemas import TokenInfo
from src.auth import utils as auth_utils
from src.auth.config import auth_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/singin')


async def get_current_token_payload(token: Annotated[str, Depends(oauth2_scheme)]) -> UserRead:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as ex:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error",
        )
    return payload


async def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} expected {token_type!r}",
    )


async def get_current_auth_user(
    get_user: Annotated[GetUser, Depends()],
    payload: dict = Depends(get_current_token_payload),
) -> UserRead:
    await validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    id: str | None = payload.get("sub")
    if user := await get_user.get_user_for_id(int(id)):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def get_current_auth_user_for_refresh(
    get_user: Annotated[GetUser, Depends()],
    payload: dict = Depends(get_current_token_payload),
) -> UserRead:
    await validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    id: str | None = payload.get("sub")
    if user := await get_user.get_user_for_id(int(id)):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def get_current_active_auth_user(
    user: Annotated[UserRead, Depends(get_current_auth_user)]
) -> UserRead:
    
    if user.is_active:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


async def validate_auth_user(
        get_user: Annotated[GetUser, Depends()],
        data_form: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> TokenInfo:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
        headers={'WWW-Authenticate': 'Bearer'},
    )
    user: UserAuth = await get_user.get_user_for_username(data_form.username)
    if not user:
        raise unauthed_exc
    
    if not auth_utils.validate_password(
        password=data_form.password,
        hash_password=user.hashed_password,
    ):
        raise unauthed_exc
    
    return await create_token_jwt(user)


async def create_token_jwt(user: UserAuth) -> TokenInfo:
    
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def refresh_token_jwt(user: UserAuth) -> TokenInfo:
    
    access_token = await create_access_token(user)

    return TokenInfo(
        access_token=access_token
    )
