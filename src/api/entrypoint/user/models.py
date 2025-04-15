from pydantic import BaseModel
from enum import StrEnum
from datetime import date


class MemberType(StrEnum):
    admin = "admin"
    member = "member"


class TokenData(BaseModel):
    username: str | None = None



