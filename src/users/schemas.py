from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int

    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserCreate(UserBase):
    hashed_password: str


class UserLogin(UserRead):
    hashed_password: str


class UserUpdate(UserCreate):
    username: str | None = None
    email: EmailStr | None = None

    is_active: bool | None = None
    is_superuser: bool | None = None
    is_verified: bool | None = None
    hashed_password: bytes | None = None