from pydantic import BaseModel
from enum import StrEnum
from typing import Optional

class MemberType(StrEnum):
    admin = "admin"
    member = "member"

class UsersBase(BaseModel):
    name: str
    date_of_birth : str
    email : str
    username : str
    password : str
    permission : MemberType
    disabled : Optional[bool] = True
    user_id : Optional[str] = None