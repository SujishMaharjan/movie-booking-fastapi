from pydantic import EmailStr, SecretStr, BaseModel
from src.entrypoints.api.user.models import MemberType
from datetime import date


class UserRegisterModel(BaseModel):
    name: str
    phone: str
    email: str
    username: str
    password: SecretStr

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
