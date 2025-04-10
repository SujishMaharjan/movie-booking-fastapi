from pydantic import BaseModel
from enum import StrEnum


class MemberType(StrEnum):
    admin = "admin"
    member = "member"


class TokenData(BaseModel):
    username: str | None = None