from pydantic import EmailStr, SecretStr, BaseModel
from src.api.entrypoint.user.models import MemberType
from datetime import date


class UserRegisterModel(BaseModel):
    name: str
    date_of_birth: date
    email: str
    username: str
    password: SecretStr
    permission: MemberType


class UserLoginModel(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
