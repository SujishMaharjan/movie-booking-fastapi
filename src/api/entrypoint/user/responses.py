from pydantic import BaseModel
from src.api.entrypoint.user.models import MemberType
from datetime import date
from src.modules.user.entity.user import UserRole

class AllUserResponse(BaseModel):
    id: str
    username: str
    name: str
    role: UserRole

class UserIdResponse(BaseModel):
    id : str
    name: str
    email : str
    username : str
    role : UserRole
