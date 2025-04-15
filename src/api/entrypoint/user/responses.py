from pydantic import BaseModel
from src.api.entrypoint.user.models import MemberType
from datetime import date

class AllUserResponse(BaseModel):
    user_id: int
    username: str
    name: str
    permission: MemberType

class UserIdResponse(BaseModel):
    user_id : int
    name: str
    date_of_birth : date
    email : str
    username : str
    permission : MemberType
