from dataclasses import dataclass
from uuid import UUID
from enum import StrEnum
from datetime import datetime

class UserRole(StrEnum):
        ADMIN = "admin"
        MEMBER = "member"

@dataclass
class User:
    id: UUID
    name: str
    phone: str
    email: str
    username: str
    hashed_password: str
    created_at: datetime
    role: UserRole

    

