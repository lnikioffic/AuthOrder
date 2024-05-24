from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from src.auth.token import create_access_token, create_refresh_token, TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.users.dependencies import valid_user_id, valid_user_username
from src.users.schemas import UserLogin, UserRead
from src.auth.schemas import TokenInfo
from src.auth import utils as auth_utils
from src.users.service import ServiceUser

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

async def get_user_by_token_sub(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        service: Annotated[ServiceUser, Depends()]
    ) -> UserRead:
    id: str | None = payload.get("sub")
    if user := await valid_user_id(int(id), service):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )
    
    
# async def get_auth_user_from_token_of_type(token_type: str):
#     async def get_auth_user_from_token(
#         payload: dict = Depends(get_current_token_payload),
#     ) -> UserRead:
#         await validate_token_type(payload, token_type)
#         return await get_user_by_token_sub()

#     return get_auth_user_from_token


# class UserGetterFromToken:
#     def __init__(self, token_type: str):
#         self.token_type = token_type

#     async def __call__(
#         self,
#         payload: dict = Depends(get_current_token_payload),
#     ):
#         await validate_token_type(payload, self.token_type)
#         return await get_user_by_token_sub()
    
# get_current_auth_user = UserGetterFromToken(ACCESS_TOKEN_TYPE)

# get_current_auth_user_for_refresh = UserGetterFromToken(REFRESH_TOKEN_TYPE)

async def get_current_auth_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        service: Annotated[ServiceUser, Depends()]
    ) -> UserRead:
    await validate_token_type(payload=payload, token_type=ACCESS_TOKEN_TYPE)
    id: str | None = payload.get("sub")
    if user := await valid_user_id(int(id), service):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


async def get_current_auth_user_for_refresh(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        service: Annotated[ServiceUser, Depends()]
    ) -> UserRead:
    await validate_token_type(payload=payload, token_type=REFRESH_TOKEN_TYPE)
    id: str | None = payload.get("sub")
    if user := await valid_user_id(int(id), service):
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
        data_form: Annotated[OAuth2PasswordRequestForm, Depends()],
        service: Annotated[ServiceUser, Depends()]
    ) -> TokenInfo:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
        headers={'WWW-Authenticate': 'Bearer'},
    )
    user: UserLogin = await valid_user_username(data_form.username, service)
    if not user:
        raise unauthed_exc
    
    if not auth_utils.validate_password(
        password=data_form.password,
        hash_password=user.hashed_password,
    ):
        raise unauthed_exc
    
    return await create_token_jwt(user)


async def create_token_jwt(user: UserLogin) -> TokenInfo:
    
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)

    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )


async def refresh_token_jwt(user: UserLogin) -> TokenInfo:
    
    access_token = await create_access_token(user)

    return TokenInfo(
        access_token=access_token
    )
