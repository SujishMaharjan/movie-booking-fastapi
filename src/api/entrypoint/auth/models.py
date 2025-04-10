from pydantic import EmailStr, SecretStr, BaseModel
from src.api.entrypoint.user.models import MemberType
from datetime import date
from typing import Optional


class UserRegisterModel(BaseModel):
    name: str
    date_of_birth : date
    email : str
    username : str
    password : str
    permission : MemberType
    user_id : Optional[int]= None
    # user_id : int | None = None


class UserLoginModel(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    username: str | None = None


