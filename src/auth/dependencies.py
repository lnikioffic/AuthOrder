from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from src.users.dependencies import GetUser
from src.users.schemas import UserAuth, UserRead
from src.auth.schemas import TokenInfo
from src.auth import utils as auth_utils

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


# def get_current_auth_user(
#     payload: dict = Depends(get_current_token_payload),
# ) -> UserRead:
#     username: str | None = payload.get("sub")
#     if user := users_db.get(username):
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="token invalid (user not found)",
#     )


def get_current_active_auth_user(
    user: Annotated[dict, Depends(get_current_token_payload)]
) -> dict:
    
    if user['sub']:
        return user
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="user inactive",
    )


async def validate_auth_user(
        user: Annotated[GetUser, Depends()],
        data_form: Annotated[OAuth2PasswordRequestForm, Depends()]
    ) -> TokenInfo:
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
        headers={'WWW-Authenticate': 'Bearer'},
    )
    user: UserAuth = await user.get_user_for_auth(data_form.username)
    if not user:
        raise unauthed_exc
    
    if not auth_utils.validate_password(
        password=data_form.password,
        hash_password=user.hashed_password,
    ):
        raise unauthed_exc
    
    return await create_token_jwt(user)


async def create_token_jwt(user: UserAuth) -> TokenInfo:
    payload = {
        'sub': str(user.id),
        'user': {
            'username': user.username,
            'email': user.email,
            'is_active': user.is_active
        }
    }
    token = auth_utils.encode_jwt(payload=payload)

    return TokenInfo(
        access_token=token
    )


